from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('draw/', include('draw.urls')),
    path('', admin.site.urls),
]
