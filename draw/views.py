import uuid
import qrcode
import io
import base64
import json
from random import sample
from django.utils import timezone  # Django의 시간대 지원
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DrawManager
from .models import DrawApplicant
from .serializers import DrawManagerSerializer
from .serializers import DrawApplicantSerializer


class DrawManagerView(APIView):
    def post(self, request):
        params = request.data.copy()
        params['uuid'] = uuid.uuid1()
        serializer = DrawManagerSerializer(data=params)
        if serializer.is_valid():
            serializer.save()

            # HTTP 링크 생성
            draw_url = f"http://127.0.0.1:8000/plag/{params['uuid']}/"

            # QR 코드 생성
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(draw_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # QR 코드를 Base64로 인코딩
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            # 응답 데이터
            response_data = serializer.data
            response_data['link'] = draw_url
            response_data['qr_code'] = qr_base64

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DrawManagerDetailView(APIView):
    def get(self, request, uuid):
        try:
            # DrawManager 가져오기
            draw_manager = DrawManager.objects.get(uuid=uuid)
            draw_manager_serializer = DrawManagerSerializer(draw_manager)

            # DrawApplicant 가져오기
            draw_applicants = DrawApplicant.objects.filter(draw_uuid=draw_manager).order_by('-is_winner', 'uuid')
            draw_applicant_serializer = DrawApplicantSerializer(draw_applicants, many=True)

            # 결과 구성
            response_data = {
                'draw_manager': draw_manager_serializer.data,
                'applicants': draw_applicant_serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except DrawManager.DoesNotExist:
            return Response({'detail': 'DrawManager not found'}, status=status.HTTP_404_NOT_FOUND)


class DrawManagerChoiceView(APIView):
    def put(self, request, uuid):
        try:
            params = request.data.copy()
            draw_manager = DrawManager.objects.get(uuid=uuid, password=params['password'])
            draw_manager_serializer = DrawManagerSerializer(draw_manager)

            if draw_manager_serializer.data:
                # 검증
                if draw_manager.state != 0:
                    return Response({'resultCode': 200, 'message': 'Draw already completed or invalid state'}, status=status.HTTP_200_OK)

                # draw_time 확인
                if draw_manager.draw_time > timezone.now():  # timezone-aware 비교
                    return Response({'resultCode': 400, 'message': 'Draw time has not passed'}, status=status.HTTP_400_BAD_REQUEST)

                # DrawManager.draw_num만큼 랜덤한 DrawApplicant 데이터를 선택
                draw_applicants = DrawApplicant.objects.filter(draw_uuid=draw_manager)
                if draw_applicants.count() < draw_manager.draw_num:
                    return Response({'resultCode': 400, 'message': 'Not enough applicants'}, status=status.HTTP_400_BAD_REQUEST)

                # 랜덤으로 draw_num 만큼의 당첨자를 선택
                winners = sample(list(draw_applicants), draw_manager.draw_num)

                # 당첨자들의 is_winner 값을 True로 업데이트
                for winner in winners:
                    winner.is_winner = True

                    try:
                        # 이메일 전송
                        subject = f"축하드립니다! 추첨에 당첨되셨습니다: {draw_manager.title}"
                        recipient_list = [winner.email]  # 당첨자의 이메일 주소
                        send_mail(subject, (draw_manager.email_form), settings.EMAIL_HOST_USER, recipient_list)
                        winner.email_state = True
                    except:
                        pass

                    winner.save()

                # DrawManager의 state를 1로 업데이트
                draw_manager.state = 1
                draw_manager.save()

                return Response({'resultCode': 200, 'message': 'success', 'winners': [winner.uuid for winner in winners]}, status=status.HTTP_200_OK)
            else:
                return Response({'resultCode': 401, 'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except DrawManager.DoesNotExist:
            return Response({'resultCode': 401, 'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'resultCode': 500, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DrawApplicantView(APIView):
    def post(self, request):
        params = request.data.copy()
        params['uuid'] = uuid.uuid1()
        serializer = DrawApplicantSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # DrawManager 객체 가져오기 (DrawApplicant의 draw_uuid를 통해 접근)
                draw_manager = DrawManager.objects.get(uuid=params['draw_uuid'])

                # DrawManager의 form 필드에서 pk 정보를 추출
                form_config = draw_manager.form
                pk_fields = form_config.get("pk", [])

                # pk 필드 기반으로 중복 신청자 여부 확인
                filter_kwargs = {"draw_uuid": draw_manager}
                for pk_field in pk_fields:
                    filter_kwargs[pk_field] = params.get(pk_field)

                # 기존 신청자 조회
                if DrawApplicant.objects.filter(**filter_kwargs).exists():
                    return Response(
                        {'resultCode': 400, 'message': 'Duplicate application detected'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # 중복이 없으면 저장
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except DrawManager.DoesNotExist:
                return Response(
                    {'resultCode': 400, 'message': 'Invalid draw_uuid'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DrawApplicantDetailView(APIView):
    def get(self, request, uuid):
        try:
            # DrawApplicant 객체 가져오기
            draw_applicant = DrawApplicant.objects.get(uuid=uuid)

            # DrawManager 객체 가져오기 (DrawApplicant의 draw_uuid를 통해 접근)
            draw_manager = draw_applicant.draw_uuid

            # DrawManager에서 특정 필드 제외 (password, email_form)
            draw_manager_data = {
                "uuid": draw_manager.uuid,
                "name": draw_manager.name,
                "title": draw_manager.title,
                "info": draw_manager.info,
                "link": draw_manager.link,
                "form": draw_manager.form,
                "state": draw_manager.state,
                "crontab": draw_manager.crontab,
                "draw_num": draw_manager.draw_num,
                "auto_email": draw_manager.auto_email,
                "limit_time": draw_manager.limit_time,
                "draw_time": draw_manager.draw_time,
            }

            # DrawApplicant 데이터 직렬화
            applicant_serializer = DrawApplicantSerializer(draw_applicant)

            # 결과 데이터 구성
            result_data = {
                "applicant": applicant_serializer.data,
                "draw_manager": draw_manager_data
            }

            return Response(result_data, status=status.HTTP_200_OK)
        except DrawApplicant.DoesNotExist:
            return Response({'detail': 'DrawApplicant not found'}, status=status.HTTP_404_NOT_FOUND)