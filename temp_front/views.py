from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from editora_api.models import BGR


def index(request):
    return render(request, 'temp_front/index.html')

def login(request):
    return render(request, 'temp_front/log-in.html')

@login_required(login_url="/log-in")
def dashboard(request):
    return render(request, 'temp_front/dashboard.html')

@login_required(login_url="/log-in")
def mylogout(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass
    logout(request)
    return redirect('/')
