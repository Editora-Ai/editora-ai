from django.urls import path, include
from . import views



urlpatterns = [
    # Homepage path
    path('', views.index, name='index'),
    path('log-in', views.login, name='login'),
    path('log-out', views.mylogout, name='logout'),
    path('sign-up', views.signup, name='signup'),
    path('password-reset', views.password_reset, name='password_reset'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/bgremoval', views.bgremoval, name='bgremoval'),
    path('dashboard/faceremoval', views.faceremoval, name='faceremoval'),
    path('dashboard/tasks', views.tasks, name='tasks'),
    path('dashboard/account', views.account, name="account"),
]
