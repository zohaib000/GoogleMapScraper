from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", home.as_view(), name="home"),
    path("twitter", twitter.as_view(), name="twitter"),
    path("currentJob", currentJob.as_view(), name="currentJob"),

    path("user_login", views.user_login, name="user_login"),
    path("signup", views.signup, name="signup"),
    path("logo", views.logo, name="logo"),

    path('verify/<str:token_coming>/', views.verify, name="verify"),
]
