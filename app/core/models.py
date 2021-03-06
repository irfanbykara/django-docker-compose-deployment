from django.db import models
from django.contrib.auth.models import User

# Create your models here.
LEVEL_CHOICES = (
    ('beginner', 'BEGINNER'),
    ('intermediate', 'INTERMEDIATE'),
    ('expert', 'EXPERT')
)


class Profile( models.Model ):
    user = models.OneToOneField( User, on_delete=models.CASCADE, null=True, )
    name = models.CharField( max_length=200, null=True )
    email = models.CharField( max_length=200, null=True )
    level = models.CharField( max_length=200, choices=LEVEL_CHOICES, null=True )
    avatar = models.ImageField( null=True, default="indir.png" )
    weight = models.IntegerField( null=True )
    height = models.IntegerField( null=True )
    bmi = models.IntegerField( null=True )
    birthday = models.DateTimeField( null=True, )
    age = models.IntegerField( null=True, )

    def __str__(self):
        return self.name


WORKOUT_CATEGORIES = (
    ('chest', 'CHEST'),
    ('biceps', 'BICEPS'),
    ('triceps', 'TRICEPS'),
    ('legs', 'LEGS'),
    ('core', 'CORE'),
    ('back', 'BACK'),
    ('shoulder', 'SHOULDER')
)


class Workout( models.Model ):
    name = models.CharField( max_length=200, null=False )
    user = models.ForeignKey( User, on_delete=models.CASCADE, blank=False, null=False )
    category = models.CharField( max_length=8, choices=WORKOUT_CATEGORIES, default='chest' )
    date = models.DateTimeField( auto_now_add=True,null=True )
    user_weight = models.IntegerField( null=True )
    user_height = models.IntegerField( null=True )
    user_bmi = models.IntegerField( null=True )

    def __str__(self):
        return self.name


class Excercise( models.Model ):
    name = models.CharField( max_length=200, null=True )
    workout = models.ForeignKey( Workout, on_delete=models.CASCADE,null=True)
    rep = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class CustomExcercise( models.Model ):
    name = models.CharField( max_length=30, null=True, )
    user = models.ForeignKey( User, on_delete=models.CASCADE, blank=False, null=False )
    category = models.CharField( max_length=30, null=True )

    def __str__(self):
        return self.name
