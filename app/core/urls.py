from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from . import views
from django.conf import settings


urlpatterns = [
    path('',views.home, name='home'),
]
