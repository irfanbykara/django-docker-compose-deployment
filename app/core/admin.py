from django.contrib import admin
from .models import Excercise, Profile,User,Workout,CustomExcercise

# Register your models here.

admin.site.unregister(User)
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Workout)
admin.site.register(Excercise)
admin.site.register(CustomExcercise)




