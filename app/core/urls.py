from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from . import views
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home, name='home'),

]
