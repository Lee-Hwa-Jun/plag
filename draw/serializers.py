from rest_framework import serializers
from .models import DrawManager
from .models import DrawApplicant


class DrawManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrawManager
        exclude = ['password']  # 'password' 필드를 제외하고 직렬화


class DrawApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrawApplicant
        exclude = ['password']  # 'password' 필드를 제외하고 직렬화