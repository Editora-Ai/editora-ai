from django.urls import path, include
from .views import ListBGR, DetailBGR


urlpatterns = [
    path('bgr/', ListBGR.as_view()),
    path('bgr/<int:pk>/', DetailBGR.as_view()),
]
