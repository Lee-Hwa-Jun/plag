from django.contrib.auth import get_user_model
import os

User = get_user_model()

# 환경 변수로부터 슈퍼유저 정보 읽기
username = os.getenv('DJANGO_SUPERUSER_USERNAME')
email = os.getenv('DJANGO_SUPERUSER_EMAIL')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

# 이미 존재하지 않는 경우에만 슈퍼유저 생성
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created.')
else:
    print(f'Superuser {username} already exists.')
