import ntpath
import requests
from itertools import chain
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404, JsonResponse
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from allauth.account.utils import send_email_confirmation
from editora_api.models import BGR, FR, PR
from user.models import User



site_key = settings.RECAPTCHA_SITE_KEY
secret_key = settings.RECAPTCHA_SECRET_KEY


class HttpResponseNoContent(HttpResponse):
    status_code = 204


def confirm_email(request, uidb64, token):
    return render(request, 'temp_front/password_reset_confirm.html')

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
    return render(request, 'temp_front/index.html', {'site_key': site_key })

@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    if request.method == 'POST':
        ### Recaptcha ###
        data = {
            'response': request.POST.get('token'),
            'secret': secret_key
        }
        resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result_json = resp.json()

        if not result_json.get('success'):
            return render(request, 'temp_front/log-in.html', {'is_robot': True, 'site_key': site_key})
        ### Recaptcha ###
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = auth.authenticate(email=email, password=password)
            auth.login(request, user)
        except:
            return HttpResponseNotFound("404")
        return redirect('/dashboard')
    else:
        return render(request, 'temp_front/log-in.html', {'site_key': site_key })

@csrf_exempt
def signup(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    if request.method == "POST":
        ### Recaptcha ###
        data = {
            'response': request.POST.get('token'),
            'secret': secret_key
        }
        resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result_json = resp.json()

        if not result_json.get('success'):
            return render(request, 'temp_front/sign-up.html', {'is_robot': True, 'site_key': site_key})
        ### Recaptcha ###
        new_user = User()
        new_user.email = request.POST.get('email')
        new_user.firstname = request.POST.get('firstname')
        new_user.lastname = request.POST.get('lastname')
        new_user.company = request.POST.get('company')
        try:
            if validate_password(request.POST.get('password1')) == None:
                new_user.set_password(request.POST.get('password1'))
        except:
            mess = {"responseText": "not good!"}
            return JsonResponse(mess, status=404)
        new_user.save()
        # confirm_mail_all_auth
        send_email_confirmation(request, new_user, True)
        return HttpResponseNoContent()
    else:
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        logout(request)
        return render(request, 'temp_front/sign-up.html', {'site_key': site_key })

def password_reset(request):
    if request.method == 'POST':
        ### Recaptcha ###
        data = {
            'response': request.POST.get('token'),
            'secret': secret_key
        }
        resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result_json = resp.json()

        if not result_json.get('success'):
            return render(request, 'temp_front/password-reset.html', {'is_robot': True, 'site_key': site_key})
        ### Recaptcha ###
        try:
            user = User.objects.get(email=request.POST.get('email'))
        except:
            mess = {"responseText": "Not correct mail!"}
            return JsonResponse(mess, status=404)
    if request.user.is_authenticated:
        return redirect('dashboard/account')
    return render(request, 'temp_front/password-reset.html', {'site_key': site_key })

@login_required(login_url="/log-in")
def dashboard(request):
    fullname = (request.user.firstname + " " + request.user.lastname).title()
    name = request.user.firstname.title()
    if request.user.company is not None:
        company = request.user.company.upper()
    else:
        company = " "
    user_bgr_tasks = BGR.objects.filter(owner=request.user).order_by('-date_created')
    user_fr_tasks = FR.objects.filter(owner=request.user).order_by('-date_created')   
    user_pr_tasks = PR.objects.filter(owner=request.user).order_by('-date_created')   
    all_tasks = list(
        sorted(
            chain(user_bgr_tasks, user_fr_tasks, user_pr_tasks),
            key=lambda objects: objects.date_created,
            reverse=True
        )
    ) 
    remaining_tasks = user_bgr_tasks.exclude(status="success").count() + user_bgr_tasks.exclude(status="success").count() + user_fr_tasks.exclude(status="success").count() + user_pr_tasks.exclude(status="success").count()
    data = {'fullname': fullname, 'name': name, 'tasks': all_tasks,
            'company': company, 'remaining_tasks': remaining_tasks}

    return render(request, 'temp_front/dashboard.html', data)

@login_required(login_url="/log-in")
def bgremoval(request):
    fullname = (request.user.firstname + " " + request.user.lastname).title()
    name = request.user.firstname.title()
    if request.user.company is not None:
        company = request.user.company.upper()
    else:
        company = " "
    data = {'fullname': fullname, 'name': name,
            'company': company }
    return render(request, 'temp_front/bgr.html', data)

@login_required(login_url="/log-in")
def faceremoval(request):
    fullname = (request.user.firstname + " " + request.user.lastname).title()
    name = request.user.firstname.title()
    if request.user.company is not None:
        company = request.user.company.upper()
    else:
        company = " "
    data = {'fullname': fullname, 'name': name,
            'company': company }
    return render(request, 'temp_front/fr.html', data)

@login_required(login_url="/log-in")
def plateremoval(request):
    if request.method == 'POST':
        if request.POST.get("clear_logo"):
            account = request.user
            account.user_logo = None
            account.save()
        else:
            try:
                image_logo = request.FILES['logo']
                account = request.user
                account.user_logo = image_logo
                account.save()
            except:
                pass
        # In return
        fullname = (request.user.firstname + " " + request.user.lastname).title()
        name = request.user.firstname.title()
        logo_image = ntpath.basename(str(request.user.user_logo))
        if request.user.company is not None:
            company = request.user.company.upper()
        else:
            company = " "
        data = {'fullname': fullname, 'name': name,
                'company': company, 'logo_image': logo_image }
        return render(request, 'temp_front/pr.html', data)
    else:
        fullname = (request.user.firstname + " " + request.user.lastname).title()
        name = request.user.firstname.title()
        logo_image = ntpath.basename(str(request.user.user_logo))
        if request.user.company is not None:
            company = request.user.company.upper()
        else:
            company = " "
        data = {'fullname': fullname, 'name': name,
                'company': company, 'logo_image': logo_image }
        return render(request, 'temp_front/pr.html', data)

@login_required(login_url="/log-in")
def tasks(request):
    fullname = (request.user.firstname + " " + request.user.lastname).title()
    name = request.user.firstname.title()
    if request.user.company is not None:
        company = request.user.company.upper()
    else:
        company = " "
    user_bgr_tasks = BGR.objects.filter(owner=request.user).order_by('-date_created')
    user_fr_tasks = FR.objects.filter(owner=request.user).order_by('-date_created')   
    user_pr_tasks = PR.objects.filter(owner=request.user).order_by('-date_created')   
    all_tasks = list(
        sorted(
            chain(user_bgr_tasks, user_fr_tasks, user_pr_tasks),
            key=lambda objects: objects.date_created,
            reverse=True
        )
    ) 
    remaining_tasks = user_bgr_tasks.exclude(status="success").count() + user_bgr_tasks.exclude(status="success").count() + user_fr_tasks.exclude(status="success").count() + user_pr_tasks.exclude(status="success").count()
    paginator = Paginator(all_tasks, 10)
    page = request.GET.get('page', 1)
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    data = {'fullname': fullname, 'name': name, 'tasks': tasks,
            'company': company, 'paginator': paginator, 'remaining_tasks': remaining_tasks}
    return render(request, 'temp_front/tasks.html', data)

@login_required(login_url="/log-in")
def account(request):
    fullname = (request.user.firstname + " " + request.user.lastname).title()
    name = request.user.firstname.title()
    lastname = request.user.lastname.title()
    email = request.user.email
    if request.user.company is not None:
        company = request.user.company.upper()
    else:
        company = " "
    user_bgr_tasks = BGR.objects.filter(owner=request.user).order_by('-date_created')
    user_fr_tasks = FR.objects.filter(owner=request.user).order_by('-date_created')   
    user_pr_tasks = PR.objects.filter(owner=request.user).order_by('-date_created')   
    all_tasks = (user_bgr_tasks.count()) + (user_fr_tasks.count()) + (user_pr_tasks.count())
    success_tasks = user_bgr_tasks.filter(status="success").count() + user_fr_tasks.filter(status="success").count() + user_pr_tasks.filter(status="success").count()
    data = {'fullname': fullname, 'name': name, 'bgr_tasks': user_bgr_tasks, 'fr_tasks': user_fr_tasks, 'pr_tasks': user_pr_tasks, 'tasks': all_tasks,
            'company': company, 'success_tasks': success_tasks, "last": lastname, "email": email}

    return render(request, 'temp_front/profile.html', data)

@login_required(login_url="/log-in")
def mylogout(request):
    logout(request)
    return redirect('/')
