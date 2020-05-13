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
    if request.user.is_authenticated:
        return redirect('/dashboard')
    return render(request, 'temp_front/log-in.html')

def signup(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass
    logout(request)
    return render(request, 'temp_front/sign-up.html')


@login_required(login_url="/log-in")
def dashboard(request):
    fullname = request.user.get_full_name().title()
    name = request.user.get_short_name().title()
    user_bgr_tasks = BGR.objects.filter(owner=request.user)
    data = {'fullname': fullname, 'name': name, 'bgr_tasks': user_bgr_tasks }
    return render(request, 'temp_front/dashboard.html', data)

@login_required(login_url="/log-in")
def mylogout(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass
    logout(request)
    return redirect('/')
