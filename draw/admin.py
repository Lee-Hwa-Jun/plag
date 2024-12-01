from django.contrib import admin
from .models import DrawManager, DrawApplicant

admin.site.register(DrawManager)
admin.site.register(DrawApplicant)