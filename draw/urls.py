# draw/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('draw-manager/', views.DrawManagerView.as_view(), name='draw-manager'),
    path('draw-manager/detail/<uuid:uuid>/', views.DrawManagerDetailView.as_view(), name='draw-manager-detail'),
    path('draw-manager/choice/<uuid:uuid>/', views.DrawManagerChoiceView.as_view(), name='draw-manager-choice'),
    path('draw-applicant/', views.DrawApplicantView.as_view(), name='draw-applicant'),
    path('draw-applicant/detail/<uuid:uuid>/', views.DrawApplicantDetailView.as_view(), name='draw-applicant-detail'),
]