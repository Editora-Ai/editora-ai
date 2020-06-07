from django.urls import path, include
from .views import ListBGR, DetailBGR, ListFR, DetailFR


urlpatterns = [
    # Background removal endpoints
    path('bgr/', ListBGR.as_view()),
    path('bgr/<int:pk>/', DetailBGR.as_view()),
    # Face removal endpoints
    path('fr/', ListFR.as_view()),
    path('fr/<int:pk>/', DetailFR.as_view()),
]
