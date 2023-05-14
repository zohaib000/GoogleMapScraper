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



