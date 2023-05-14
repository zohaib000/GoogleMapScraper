from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("/", twitter.as_view(), name="twitter"),
    path("currentJob", currentJob.as_view(), name="currentJob"),
]
