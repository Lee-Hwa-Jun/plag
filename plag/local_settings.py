from plag.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # MySQL 백엔드 사용
        'NAME': config('MYSQL_DATABASE'),      # .env 파일에서 로드
        'USER': config('MYSQL_USER'),          # .env 파일에서 로드
        'PASSWORD': config('MYSQL_PASSWORD'),  # .env 파일에서 로드
        'HOST': 'localhost',                   # Docker Compose의 MariaDB 서비스 이름
        'PORT': '3306',                        # MariaDB 기본 포트
    }
}