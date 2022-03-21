from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Workout,User,Profile,Excercise
from rest_framework import status
from .serializers import WorkoutSerializers, UserSerializer,ProfileSerializer,ExcerciseSerializer
from ..utils import encrypt_string,get_records,list_operator
from django.contrib.auth.hashers import make_password, check_password

@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/workouts/<str:pk>',
        'POST /api/addworkout',
        'POST /api/login',
        'GET /api/get-excercises/<str:pk>',
        'GET /api/get-records',
        'POST /api/add-excercise',
        'POST /api/register-user',
        'GET /api/get-users',
        'GET /api/get-workouts-by-user/<str:pk>',
        'GET /api/delete-excercise/<str:pk>',

    ]
    return Response(routes,)

@api_view(['GET'])
def get_workouts(request):
    workouts = Workout.objects.all()
    serializer = WorkoutSerializers(workouts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_workouts_by_user(request,pk):
    user = User.objects.get(id=pk)
    workouts = Workout.objects.filter(user=user)
    serializer = WorkoutSerializers(workouts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_workout(request,pk):
    workout = Workout.objects.get(id=pk)
    serializer = WorkoutSerializers(workout, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def add_workout(request):
    serializer = WorkoutSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    username_posted = request.data['username']
    password_posted = request.data['password']
    password_posted_enc = encrypt_string(password_posted)
    user_found = User.objects.get( username = username_posted )
    serializer =UserSerializer(user_found,many=False)
    profile = Profile.objects.get(user=user_found)
    profile_serialized = ProfileSerializer(profile,many=False)
    if user_found != None:
        if (check_password(password_posted,user_found.password)):
            return Response(profile_serialized.data, status=status.HTTP_202_ACCEPTED)
    return Response(False, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_excercises(request,pk):
    try:
        workout = Workout.objects.get(id=pk)
        excercises = Excercise.objects.filter(workout=workout)
        print(excercises)
        serializer = ExcerciseSerializer(excercises, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(False,status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_records(request):
    try:
        records = []
        records = list_operator( Excercise.objects.filter( name='BENCH PRESS' ).order_by( 'weight' ), records )
        records = list_operator( Excercise.objects.filter( name='SQUAT' ).order_by( 'weight' ), records )
        records = list_operator( Excercise.objects.filter( name='DEADLIFT' ).order_by( 'weight' ), records )
        records = list_operator( Excercise.objects.filter( name='OVERHEAD PRESS' ).order_by( 'weight' ), records )    # serializer = ExcerciseSerializer( records, many=True )
        serializer = ExcerciseSerializer(records,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_excercise(request):
    serializer = ExcerciseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(id=serializer.data['id'])
        Profile.objects.create(
            user=user,
            name=serializer.data['username']
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def delete_excercise(request,pk):
    excercise = Excercise.objects.get(id=pk)
    excercise.delete()
    return Response(status=status.HTTP_200_OK)

# {"username":"irfanbykara","password":"18Evler!"}