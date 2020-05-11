from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings


def index(request):
    return render(request, 'temp_front/index.html')

def login(request):
    return render(request, 'temp_front/log-in.html')