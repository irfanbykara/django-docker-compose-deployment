from django.urls import path
from . import views

urlpatterns = [
    path('',views.get_routes),
    path( 'workouts/', views.get_workouts ),
    path( 'workouts/<str:pk>/', views.get_workout ),
    path('workouts/<str:pk>/', views.get_workout),
    path('addworkout/', views.add_workout),
    path( 'login/', views.login ),
    path( 'get-excercises/<str:pk>', views.get_excercises ),
    path( 'get-records/', views.get_records ),
    path( 'get-records/', views.get_records ),
    path( 'add-excercise/', views.add_excercise ),
    path( 'register-user/', views.register_user ),
    path( 'get-users/', views.get_users ),
    path( 'get-workouts-by-user/<str:pk>', views.get_workouts_by_user ),
    path( 'delete-excercise/<str:pk>', views.delete_excercise ),

]