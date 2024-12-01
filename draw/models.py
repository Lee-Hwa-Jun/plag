from django.db import models
import uuid


class DrawManager(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    title = models.CharField(max_length=100)
    info = models.CharField(max_length=500)
    link = models.JSONField()  # MariaDB에서도 JSON 필드를 사용하려면 이렇게 사용
    form = models.JSONField()  # 동일하게 JSON 필드 사용
    state = models.SmallIntegerField(default=0)
    crontab = models.BooleanField(default=False)
    draw_num = models.IntegerField()
    auto_email = models.BooleanField(default=False)
    email_form = models.TextField()
    limit_time = models.DateTimeField()
    draw_time = models.DateTimeField()
    delete_time = models.DateTimeField()

    def __str__(self):
        return self.title


class DrawApplicant(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # 신청자의 uuid
    draw_uuid = models.ForeignKey(DrawManager, on_delete=models.CASCADE, related_name='applicants')  # 주최자의 uuid
    name = models.CharField(max_length=100)  # 신청자의 이름
    password = models.CharField(max_length=255)  # 신청 현황 조회용 비밀번호
    email = models.EmailField(max_length=254, blank=False, null=True)
    email_state = models.BooleanField(default=False)
    is_winner = models.BooleanField(default=False)  # 당첨자인지 여부
    form_1 = models.CharField(max_length=255, blank=True, null=True)  # 신청 양식에 따른 항목 저장값1
    form_2 = models.CharField(max_length=255, blank=True, null=True)  # 신청 양식에 따른 항목 저장값2
    form_3 = models.CharField(max_length=255, blank=True, null=True)  # 신청 양식에 따른 항목 저장값3
    form_4 = models.CharField(max_length=255, blank=True, null=True)  # 신청 양식에 따른 항목 저장값4
    form_5 = models.CharField(max_length=255, blank=True, null=True)  # 신청 양식에 따른 항목 저장값5
    form_6 = models.CharField(max_length=255, blank=True, null=True)  # 신청 양식에 따른 항목 저장값6
    form_7 = models.CharField(max_length=255, blank=True, null=True)  # 신청 양식에 따른 항목 저장값7
    form_8 = models.CharField(max_length=255, blank=True, null=True)  # 신청 양식에 따른 항목 저장값8
    form_9 = models.CharField(max_length=255, blank=True, null=True)  # 신청 양식에 따른 항목 저장값9
    form_10 = models.CharField(max_length=255, blank=True, null=True)  # 신청 양식에 따른 항목 저장값10

    def __str__(self):
        return f'{self.name} - {self.draw_uuid.title}'
