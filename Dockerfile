# 베이스 이미지 설정
FROM python:3.10-slim

# 작업 디렉토리 생성
WORKDIR /app

# 필요 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 복사
COPY . .

# 정적 파일 모으기
RUN python manage.py collectstatic --noinput

# Django 애플리케이션 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "plag.wsgi:application"]
