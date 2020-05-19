from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from editora_api.models import BGR


def index(request):
    if request.method == 'POST':
        data = request.POST.copy()
        from_email = data.get('from_email')
        message = data.get('message')
        message = message + "  " + "Sender: " + from_email
        send_mail(subject="Service Feedback",
                    from_email=from_email,
                    message=message,
                    recipient_list=['editoraaiteam@gmail.com'],
                    )
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
    fullname = (request.user.firstname + " " + request.user.lastname).title()
    name = request.user.firstname.title()
    company = request.user.company.upper()
    user_bgr_tasks = BGR.objects.filter(owner=request.user).order_by('-date_created')[:5]
    data = {'fullname': fullname, 'name': name, 'bgr_tasks': user_bgr_tasks,
            'company': company}

    return render(request, 'temp_front/dashboard.html', data)

@login_required(login_url="/log-in")
def bgremoval(request):
    fullname = (request.user.firstname + " " + request.user.lastname).title()
    name = request.user.firstname.title()
    company = request.user.company.upper()
    data = {'fullname': fullname, 'name': name,
            'company': company }
    return render(request, 'temp_front/bgr.html', data)

@login_required(login_url="/log-in")
def tasks(request):
    fullname = (request.user.firstname + " " + request.user.lastname).title()
    name = request.user.firstname.title()
    company = request.user.company.upper()
    user_bgr_tasks = BGR.objects.filter(owner=request.user).order_by('-date_created')
    paginator = Paginator(user_bgr_tasks, 10)
    page = request.GET.get('page', 1)
    try:
        bgrs = paginator.page(page)
    except PageNotAnInteger:
        bgrs = paginator.page(1)
    except EmptyPage:
        bgrs = paginator.page(paginator.num_pages)
    data = {'fullname': fullname, 'name': name, 'bgr_tasks': bgrs,
            'company': company, 'paginator': paginator}
    return render(request, 'temp_front/tasks.html', data)

@login_required(login_url="/log-in")
def account(request):
    fullname = (request.user.firstname + " " + request.user.lastname).title()
    name = request.user.firstname.title()
    lastname = request.user.lastname.title()
    email = request.user.email
    company = request.user.company.upper()
    user_bgr_tasks = BGR.objects.filter(owner=request.user).order_by('-date_created')
    success_tasks = user_bgr_tasks.filter(status="success")
    data = {'fullname': fullname, 'name': name, 'bgr_tasks': user_bgr_tasks,
            'company': company, 'success_tasks': success_tasks, "last": lastname, "email": email}

    return render(request, 'temp_front/profile.html', data)

@login_required(login_url="/log-in")
def mylogout(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass
    logout(request)
    return redirect('/')
