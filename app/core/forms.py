from django.forms import ModelForm
from .models import Excercise, User, Workout,Profile,CustomExcercise
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms.widgets import DateInput

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1', 'password2']


class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['name','category']
        exclude = ['excercise']


class ExcerciseForm(ModelForm):
    class Meta:
        model = Excercise
        fields = '__all__'
        exclude = ['workout','name','video','video_requests']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user','name','email','bmi','age']
        widgets = {
            'birthday': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       } ),
        }


class CustomExcerciseForm(ModelForm):
    class Meta:
        model = CustomExcercise
        fields = '__all__'
        exclude = ['user','category']




