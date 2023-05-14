from django.http.response import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.http import JsonResponse
from home.gpt import find
from home.forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import *
from django.core.mail import send_mail
from email.mime import multipart
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.contrib import messages
import uuid
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash


def check_ajax(r):
    if r.headers.get('X-Requested-With') == 'XMLHttpRequest':
        is_ajax = True
    else:
        is_ajax = False
    return is_ajax


class currentJob(View):
    def get(self, request):
        query = request.GET.get('query')
        job = JOBS.objects.filter(user=str(request.user), name=query).values().last()
        return JsonResponse({'job': job})


class home(View):
    def get(self, request):
        return render(request, 'home/index.html')


class twitter(View):
    def get(self, request):
        if request.user.is_authenticated:
            if check_ajax(request):
                query = request.GET.get('query')
                emails = request.GET.get('emails')
                method = request.GET.get('method')
                print(query, emails, method)
                response = find(query, emails, method, JOBS, request.user)
                print(response)
                return JsonResponse({'input': query, 'output': response})
            return render(request, 'home/twitter.html')
        else:
            return HttpResponseRedirect("/user_login")


def signup(request):
    if request.method == "POST":
        reg_user = request.POST.get('username')
        reg_email = request.POST.get('email')
        fm = RegisterForm(request.POST)
        if fm.is_valid():
            fm.save()
            email_token = str(uuid.uuid4())
            data = email_verify(user=reg_user, token=email_token)
            data.save()
            subject = 'Verify your Email to Login into Fableey!'
            message = f'Hi {reg_user},\n Thank you for registering in Fableey ,the world largest investing and earning platform.\n You can get your projects Done easily with Huge traffic of Fableey.\n As you have become member of Fableey. Now it is time to Verify your account to get Started. \n \n \n Click on Link to verify your account.  http://localhost:8000/verify/{email_token}/ \n \n Regards. \n Fableey team!'
            msg = MIMEMultipart()
            msg['From'] = 'fablyteam@gmail.com'
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.starttls()
            server.login('fablyteam@gmail.com', 'vvpyklnooevpzgbs')
            server.sendmail('fablyteam@gmail.com',
                            reg_email, msg.as_string())
            server.quit()
            # saving profile data
            messages.success(
                request, "Your Account has been created successfully!.Check your Email to verify your Account!")
            return HttpResponseRedirect("/user_login")
    else:
        fm = RegisterForm()
        return render(request, "home/signup.html", {"form": fm})
    return render(request, "home/signup.html", {"form": fm})


def user_login(request):
    if request.method == "POST":
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data["username"]
            upass = fm.cleaned_data["password"]
            user = authenticate(username=uname, password=upass)
            if user is not None:
                log_user = email_verify.objects.filter(user=uname).latest('id')
                if (log_user.is_verified):
                    login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    return render(request, "home/login.html", {'form': fm, 'error': 'We have sent you a confirmation Email,Please verify your Email to Login.', 'diplay': 'block'})
    else:
        fm = AuthenticationForm()
        return render(request, "home/login.html", {"form": fm})
    return render(request, "home/login.html", {"form": fm})


def logo(request):
    logout(request)
    return HttpResponseRedirect("/user_login")


def verify(request, token_coming):
    obj = email_verify.objects.get(token=token_coming)
    obj.is_verified = True
    obj.save()
    return render(request, 'home/verification_success.html')
