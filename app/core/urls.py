from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from . import views
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.login_page, name='login'),
    path( 'personal_stats/', views.personal_stats, name='personal-stats' ),
    path( 'global_stats/', views.global_stats, name='global-stats' ),
    path('video-request-notification/',views.video_request_notification,name='video-request-notification'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path( 'delete-excercise/<str:pk>', views.delete_excercise, name='delete-excercise' ),
    path( 'update-excercise/<str:pk>', views.update_excercise, name='update-excercise' ),
    path( 'upload-video/<str:pk>', views.upload_video, name='upload-video' ),
    path( 'show-video/<str:pk>', views.show_video, name='show-video' ),
    path( 'request-video/<str:pk>', views.request_video, name='request-video' ),
    path('create-workout/', views.create_workout, name='create-workout'),
    path('add-workout/<str:pk>', views.workout_page, name='workout-page'),
    path('workout/<str:pk>', views.workout_main, name='workout-main'),
    path( 'delete-workout/<str:pk>', views.delete_workout, name='delete-workout'),
    path( 'workout-detail/<str:pk>', views.workout_detail, name='workout-detail'),
    path( 'create-excercise/<str:pk>', views.create_excercise, name='create-excercise'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('add-custom-excercise/<str:pk>', views.add_custom_excercise, name='add-custom-excercise'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)