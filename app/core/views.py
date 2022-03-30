from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ExcerciseForm, MyUserCreationForm, WorkoutForm, ProfileForm, CustomExcerciseForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Excercise, Profile, User, Workout, CustomExcercise
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Max
from .utils import *
import datetime
from datetime import date
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Count


# Create your views here.
def home(request):
    page = 'home'
    if request.user.is_authenticated:

        if request.method == 'POST':
            workout = Workout.objects.create(
                user=request.user,
                category=request.POST.get( 'category' ),
                name=request.POST.get( 'name' ),
                user_weight=request.user.profile.weight,
                user_height=request.user.profile.height,
                user_bmi=request.user.profile.bmi
            )
            workout.save()
            return redirect( 'workout-detail', pk=workout.id )
        all_workouts = Workout.objects.all()
        if request.user.profile.height != None and request.user.profile.weight != None and request.user.profile.bmi != None:
            increasing_bmi, avg_bmi = get_bmi_avg( all_workouts, request )
            increasing_height, avg_height = get_height_avg( all_workouts, request )
            increasing_weight, avg_weight = get_weight_avg( all_workouts, request )
        else:
            increasing_bmi, avg_bmi = True, None
            increasing_height, avg_height = True, None
            increasing_weight, avg_weight = True, None
        q = request.GET.get( 'q' ) if request.GET.get( 'q' ) != None else ''
        q = request.GET.get( 'q' ) if request.GET.get( 'q' ) != None else ''
        workouts = Workout.objects.filter(
            Q( date__icontains=q ) | Q( category__icontains=q )
        )
        profile = Profile.objects.get( user=request.user )
        categories = get_categories()
        records = get_records()
        workouts = workouts.filter( user=request.user ).order_by( '-date' )
        form = WorkoutForm()
        excercises = Excercise.objects.filter(workout__user=request.user)
        labels, data = get_primary_records_by_user( request )
        all_records_by_user = get_all_records_by_user( request )
        fav_cat, workout_per_week, avg_strength = quick_stats(request)
        context = {'workouts': workouts, 'profile': profile, 'categories': categories, 'records': records,
                   'labels': labels, 'data': data, 'all_records_by_user': all_records_by_user,
                   'form': form,
                   'page': page,
                   'avg_strength':avg_strength,
                   'increasing_bmi': increasing_bmi,
                   'increasing_height': increasing_height,
                   'increasing_weight': increasing_weight,
                   'workout_per_week':workout_per_week,
                   'fav_cat':fav_cat}

        return render( request, 'core/home.html', context )
    else:
        workouts = {}
        context = {'workouts': workouts}
        return render( request, 'core/home.html', context )


def create_workout(request):
    data = dict()
    if request.method == 'POST':
        print( 'here is the formmm' )
        form = WorkoutForm( request.POST )

        if form.is_valid():

            workout = form.save( commit=False )
            name = workout.name
            category = workout.category
            user = request.user
            bmi = user.profile.bmi
            height = user.profile.height
            weight = user.profile.weight
            Workout.objects.create(
                name=name,
                user=user,
                category=category,
                user_weight=weight,
                user_height=height,
                user_bmi=bmi
            )

            data['form_is_valid'] = True
            workouts = Workout.objects.filter( user=request.user ).order_by( '-date' )
            data['html_excercise_list'] = render_to_string( 'core/partial_workout_list.html', {
                'workouts': workouts
            } )
            messages.success( request, 'Workout added successfully.' )

        else:
            data['form_is_valid'] = False

    form = WorkoutForm()

    context = {'form': form, }
    data['html_form'] = render_to_string( 'core/partial_create_workout.html',
                                          context,
                                          request=request
                                          )
    return JsonResponse( data )


def login_page(request):
    page = 'login'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect( 'home' )
    if request.method == 'POST':
        username = request.POST.get( 'username' ).lower()
        password = request.POST.get( 'password' )
        remember_me = request.POST.get('rememberme')
        try:
            user = User.objects.get( username=username )

        except:
            messages.error( request, 'User does not exist.' )
        user = authenticate( request, username=username,
                             password=password )
        if user is not None:
            login( request, user )
            if not remember_me:
                request.session.set_expiry( 0 )
            return redirect( 'home' )
        else:
            messages.error( request, 'Username or password is wrong.' )
    try:
        return render( request, 'core/login_register.html', context )
    except Exception as e:
        return HttpResponse( e )

def logout_user(request):
    logout( request )
    return redirect( 'home' )


def register_user(request):
    page = 'register'
    form = MyUserCreationForm()

    context = {'page': page, 'form': form}
    if request.method == 'POST':
        form = MyUserCreationForm( request.POST )
        if form.is_valid():
            user = form.save( commit=False )
            user.username = user.username.lower()
            username = user.username
            email = user.email
            user.save()
            login( request, user )
            return redirect( 'home' )
        else:
            for error in dict( form.errors ).values():
                messages.error( request, error, )

    return render( request, 'core/login_register.html', context )


@login_required( login_url='login' )
def workout_page(request, pk):
    form = ExcerciseForm()
    if request.method == 'POST':
        excercise = Excercise.objects.create(
            name=request.POST.get( 'excercise_name' ),
            rep=request.POST.get( 'rep' ),
            weight=request.POST.get( 'weight' ),
            workout=Workout.objects.get( id=pk )
        )

        return redirect( 'workout-main', pk=pk )

    page = 'create_excercise'
    workout = Workout.objects.get( id=pk )
    related_excercises = get_excercise_categories( user=request.user, category=workout.category )[workout.category]
    context = {'form': form, 'related_excercises': related_excercises, 'page': page, 'workout': workout}

    try:
        return render( request, 'core/workout_detail.html',
                       context
                       )
    except Exception as e:
        return HttpResponse(e)


def workout_main(request, pk):
    workout = Workout.objects.get( id=pk )
    excercises = workout.excercise_set.all()
    record_list = []
    abs_pr_list = []

    for excercise in excercises:
        max_excercise = Excercise.objects.filter( name=excercise.name ).order_by( '-weight' )[:1].get()
        if not max_excercise in abs_pr_list:
            abs_pr_list.append( max_excercise )
        related_excercises = Excercise.objects.filter( name=excercise.name )
        for related_excercise in related_excercises:

            if related_excercise.rep * related_excercise.weight < excercise.rep * excercise.weight:
                record_list.append( excercise.id )
    context = {'workout': workout, 'excercises': excercises, 'record_list': record_list, 'abs_pr_list': abs_pr_list,
               'page': page}
    return render( request, 'core/workout_detail.html', context )


@login_required()
def delete_workout(request, pk):
    workout = Workout.objects.get( id=pk )
    if request.method == 'POST':
        workout.delete()
        return redirect( 'home' )


@login_required()
def workout_detail(request, pk):
    page = 'workout_detail'
    workout = Workout.objects.get( id=pk )
    excercises = workout.excercise_set.all()
    all_workouts = Workout.objects.all()

    weight_change, weight_change_bool, height_change, height_change_bool, bmi_change, bmi_change_bool = attribute_change_check(
        request, workout )
    print( f'Here is the height change:{height_change}' )
    excercises = Excercise.objects.filter( workout=workout )
    abs_pr_list, record_list, labels, data = get_related_records( excercises )
    context = {'excercises': excercises, 'workout': workout, 'abs_pr_list': abs_pr_list, 'labels': labels, 'data': data,
               'weight_change': weight_change,
               'weight_change_bool': weight_change_bool,
               'height_change': height_change,
               'height_change_bool': height_change_bool,
               'bmi_change': bmi_change,
               'bmi_change_bool': bmi_change_bool,
               'page': page}
    try:
        return render(request, 'core/workout_detail.html', context )
    except Exception as e:
        return HttpResponse(e)


@login_required
def profile(request, pk):
    page = 'profile'
    user = User.objects.get( id=pk )
    profile = Profile.objects.get( user=user )
    form = ProfileForm( instance=profile )
    context = {'form': form, 'page': page}
    if request.method == 'POST':
        form = ProfileForm( request.POST, request.FILES, instance=profile )
        weight = int( request.POST.get( 'weight' ) )
        height = int( request.POST.get( 'height' ) ) / 100
        bmi = weight / (height * height)
        current_year = datetime.datetime.now().year
        given_age = profile.birthday.year if profile.birthday != None else int(
            request.POST.get( 'birthday' ).split( '-' )[0] )
        current_age = current_year - given_age
        if form.is_valid():
            profile.bmi = bmi
            profile.age = current_age
            profile.save()
            form.save()

            return redirect( 'home', )

    return render( request, 'core/profile.html', context )


@login_required
def add_custom_excercise(request, pk):
    form = CustomExcerciseForm()
    workout = Workout.objects.get( id=pk )

    context = {'form': form, 'workout': workout}

    if request.method == 'POST':
        user = request.user
        category = workout.category
        custom_excercises = CustomExcercise.objects.filter( user=user, category=workout.category )
        is_created = False
        for ex in custom_excercises:
            if ex.name == request.POST.get( 'name' ):
                is_created = True
                break
        if is_created:
            print( 'this instance is already created...' )
            messages.error( request, 'This excercise is already created...' )
        else:
            messages.success( request, 'New excercise category successfully added!' )
            CustomExcercise.objects.create(
                name=request.POST.get( 'name' ),
                category=category,
                user=user,
            )
            return redirect( 'workout-detail', pk=workout.id )

    return render( request, 'core/add_custom_excercise.html', context )


@login_required
def create_excercise(request, pk):
    data = dict()
    workout = Workout.objects.get( id=pk )

    if request.method == 'POST':
        print( 'here is the formmm' )
        form = ExcerciseForm( request.POST )

        if form.is_valid():
            print( 'Hello Worlds' )
            excercise = form.save( commit=False )
            excercise.workout = workout
            name = request.POST.get( 'excercise_name' )
            Excercise.objects.create(
                name=name,
                rep=excercise.rep,
                weight=excercise.weight,
                workout=excercise.workout
            )
            data['form_is_valid'] = True
            excercises = Excercise.objects.filter( workout=workout )
            print( data['form_is_valid'] )
            data['html_excercise_list'] = render_to_string( 'core/partial_excercise_list.html', {
                'excercises': excercises
            } )

        else:
            print( 'Form is not valid....' )
            data['form_is_valid'] = False

    form = ExcerciseForm()

    related_excercises = get_excercise_categories( user=request.user, category=workout.category )[workout.category]

    context = {'form': form, 'workout': workout, 'related_excercises': related_excercises}
    data['html_form'] = render_to_string( 'core/partial_create_excercise.html',
                                          context,
                                          request=request
                                          )
    return JsonResponse( data )


@login_required( login_url='login' )
def delete_excercise(request, pk):
    data = dict()
    excercise = Excercise.objects.get( id=pk )
    print( 'Hello from the delete function...' )
    if request.method == 'POST':
        print( 'Got the excercise...' )
        workout = excercise.workout

        excercise.delete()
        print( 'Excercise deleted' )
        excercises = Excercise.objects.filter( workout=workout )

        data['html_excercise_list'] = render_to_string( 'core/partial_excercise_list.html', {
            'excercises': excercises
        } )
        data['form_is_valid'] = True

    context = {'excercise': excercise}
    data['html_form'] = render_to_string( 'core/partial_delete_excercise.html',
                                          context=context,
                                          request=request
                                          )

    return JsonResponse( data )


def update_excercise(request, pk):
    data = dict()
    excercise = Excercise.objects.get( id=pk )
    workout = excercise.workout
    if request.method == 'POST':
        form = ExcerciseForm( request.POST, instance=excercise )
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            excercises = Excercise.objects.filter( workout=workout )
            print( data['form_is_valid'] )
            data['html_excercise_list'] = render_to_string( 'core/partial_excercise_list.html', {
                'excercises': excercises
            } )
    else:
        form = ExcerciseForm( instance=excercise )
    context = {'form': form, 'excercise': excercise}
    data['html_form'] = render_to_string( 'core/partial_update_excercise.html',
                                          context,
                                          request=request )
    return JsonResponse( data )


