from django.urls import path, include
from . import views


urlpatterns = [
    # Homepage path
    path('', views.index, name='index'),

]
