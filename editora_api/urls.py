from django.urls import path, include
from .views import ListBGR, DetailBGR, ListFR, DetailFR


urlpatterns = [
    path('bgr/', ListBGR.as_view()),
    path('bgr/<int:pk>/', DetailBGR.as_view()),
    path('fr/', ListFR.as_view()),
    path('fr/<int:pk>/', DetailFR.as_view()),
]
