FROM python:3.10

WORKDIR /app

# 필수 빌드 도구 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    && apt-get clean

# pip 최신 버전으로 업데이트
RUN pip install --upgrade pip

# 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --use-pep517 -r requirements.txt

# 애플리케이션 복사
COPY . .

# Django 명령 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "plag.wsgi:application"]
