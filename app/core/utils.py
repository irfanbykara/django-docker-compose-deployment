from .models import CustomExcercise,Workout,Excercise
import hashlib
from django.db.models import Count
import datetime
from datetime import date


def get_excercise_categories(user,category):

    chest = ['BARBELL BENCH PRESS', 'CABLE FLY', 'INCLINE BENCH PRESS', 'DUMBBELL BENCH PRESS', 'DECLINE PRESS',
             'MACHINE CHEST PRESS', 'DIPS', 'CHEST FLY', 'DUMBBELL PULLOVER', 'MACHINE FLY']
    legs = ['LEG EXTENSION', 'BARBELL BACK SQUAT', 'CALF RAISE', 'BARBELL FRONT SQUAT', 'DEADLIFT', 'LUNGE',
            'LEG PRESS', 'LEG CURL']
    back = ['PULL UP', 'BARBELL ROW', 'DUMBBELL ROW', 'DEADLIFT', 'LATPULL DOWN', 'PULLOVER', 'CABLE ROW']
    biceps = ['BARBELL CURL', 'DUMBBELL CURL', 'HAMMER CURL', 'CABLE CURL', ]
    triceps = ['SKULL CRUSHER', 'CLOSE GRIP BENCH PRESS', 'DIPS', ]
    core = ['SIT UP', 'PLANK', 'RUSSIAN TWIST', 'HEEL TOUCH', 'MOUNTAIN CLIMBER', 'SIDE PLANK']
    shoulder = ['MILITARY PRESS', 'LATERAL RAISE', 'DUMBBELL PRESS', 'BENT OVER RAISE', 'FRONT RAISE', 'UPRIGHT ROW']
    custom_excercises = CustomExcercise.objects.filter( user=user, category=category)
    for custom_excercise in custom_excercises:
        if category == 'chest':
            chest.append( custom_excercise.name )

        elif category == 'legs':
            legs.append( custom_excercise.name )
        elif category == 'back':
            back.append( custom_excercise.name )

        elif category == 'biceps':
            biceps.append( custom_excercise.name )

        elif category == 'triceps':
            triceps.append( custom_excercise.name )

        elif category == 'core':
            core.append( custom_excercise.name )

        elif category == 'shoulder':
            shoulder.append( custom_excercise.name )
    return {'chest':chest,
            'legs':legs,
            'back':back,
            'biceps':biceps,
            'triceps':triceps,
            'core':core,
            'shoulder':shoulder}

def get_categories():
    category_list = Workout.objects.values( 'category' ).distinct()
    categories = []
    for val in category_list.values():
        if val['category'] not in categories:
            categories.append( val['category'] )
    return categories


def get_records():

    records = []
    records=list_operator(Excercise.objects.filter( name='BARBELL BENCH PRESS' ).order_by( 'weight' ),records)
    records=list_operator(Excercise.objects.filter( name='SQUAT' ).order_by( 'weight' ),records)
    records=list_operator(Excercise.objects.filter( name='DEADLIFT' ).order_by( 'weight' ),records)
    records=list_operator(Excercise.objects.filter( name='OVERHEAD PRESS' ).order_by( 'weight' ),records)
    return records



def get_primary_records_by_user(request):
    records_by_user = []
    labels = []
    data = []
    name_list = ['BARBELL BENCH PRESS','SQUAT','DEADLIFT','OVERHEAD PRESS']
    for name in name_list:
        if Excercise.objects.filter(workout__user=request.user, name=name ).order_by( 'weight' )!=None:
            excercise = Excercise.objects.filter(workout__user=request.user, name=name ).order_by( 'weight' )
            records_by_user = list_operator(excercise,records_by_user)

    for record in records_by_user:
        labels.append(record.name)
        data.append(record.weight)
    return labels,data

def get_all_records_by_user(request):
    all_records_by_user = []
    added_name_list = []
    if Excercise.objects.filter(workout__user=request.user, ).order_by( 'weight' )!=None:
        excercises = Excercise.objects.filter(workout__user=request.user, ).order_by( 'weight' )
        for excercise in excercises:
            if excercise.name not in added_name_list:
                all_records_by_user.append(excercise)
                added_name_list.append(excercise.name)

    return all_records_by_user

def list_operator(single_list,final_list):
    if  len(single_list)>0:
        final_list.append(single_list[0])
    return final_list




def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def get_related_records(excercises):
    abs_pr_list = []
    record_list = []
    labels = []
    data = []

    for excercise in excercises:
        max_excercise = Excercise.objects.filter(name=excercise.name).order_by('-weight')[:1].get()
        if not max_excercise in abs_pr_list:
            abs_pr_list.append(max_excercise)
        related_excercises = Excercise.objects.filter(name=excercise.name)
        for related_excercise in related_excercises:

            if related_excercise.rep*related_excercise.weight<excercise.rep*excercise.weight:
                record_list.append(excercise.id)
    for abs_pr in abs_pr_list:
        temp_dict = dict()
        temp_dict['x'] = abs_pr.weight
        temp_dict['y'] = abs_pr.rep
        data.append(temp_dict)
        labels.append(abs_pr.name)
    return abs_pr_list,record_list,labels,data

def get_weight_avg(workouts,request):

    weight_list = []
    if workouts:
        for workout in workouts:
            if workout.user_weight!=None:
                weight_list.append(int(workout.user_weight))
    if len(weight_list)>0:
        avg = sum(weight_list) / len(weight_list)
    else:
        avg = 0
    if request.user.profile.weight>avg:
        return True,avg
    else:
        return False,avg

def get_height_avg(workouts,request):

    height_list = []
    if workouts:
        for workout in workouts:
            if workout.user_height!=None:

                height_list.append(int(workout.user_weight))
    if len(height_list)>0:
        avg = sum(height_list) / len(height_list)
    else:
        avg = 0
    if request.user.profile.height > avg:
        return True,avg
    else:
        return False,avg


def get_bmi_avg(workouts,request):

    bmi_list = []
    if workouts:
        for workout in workouts:
            if workout.user_bmi!=None:

                bmi_list.append(int(workout.user_bmi))
    if len(bmi_list)>0:
        avg = sum(bmi_list) / len(bmi_list)
    else:
        avg = 0
    if request.user.profile.bmi> avg:
        return True,avg
    else:
        return False,avg

def attribute_change_check(request,workout):
    weight_change_bool = False
    height_change_bool = False
    bmi_change_bool = False

    try:
        current_weight = request.user.profile.weight
        current_height = request.user.profile.height
        current_bmi = request.user.profile.bmi

        related_weight =workout.user_weight
        related_bmi =workout.user_bmi
        related_height =workout.user_height


        weight_change = abs(round((current_weight - related_weight) / current_weight,1))*100
        bmi_change = abs(round((current_bmi - related_bmi) / current_bmi,1))*100
        height_change = abs(round((current_height - related_height) / current_height,1))*100

        if weight_change>0:
            weight_change_bool = True
        if height_change>0:
            height_change_bool = True
        if bmi_change >0:
            bmi_change_bool = True

        return weight_change,weight_change_bool,height_change,height_change_bool,bmi_change,bmi_change_bool

    except:
        weight_change=0
        weight_change_bool=True
        height_change = 0
        height_change_bool=True
        bmi_change = 0
        bmi_change_bool=True
        return weight_change,weight_change_bool,height_change,height_change_bool,bmi_change,bmi_change_bool


def quick_stats(request):

    try:
        workouts = Workout.objects.filter( user=request.user ).order_by( '-date' )

        #This is the workout that is done most frequently.
        fav_cat = workouts.filter( user=request.user ).values( 'category' ).annotate( count=Count( 'category' ) ).order_by(
            "-count" )[0]['category']

        # How often do yo train a week
        workout_count = workouts.filter( user=request.user ).count()
        first_workout = workouts.filter( user=request.user ).order_by( "date" )[0].date
        current_time = datetime.datetime.now()
        d0 = date( first_workout.year, first_workout.month, first_workout.day )
        d1 = date( current_time.year, current_time.month, current_time.day )
        time_delta_week = (d1 - d0).days / 7
        workout_per_week = int( workout_count / time_delta_week )

        #Avg of 4 main excercise's max lifts.
        all_records_by_user = get_all_records_by_user( request )
        record_weights = []
        for record in all_records_by_user:
            record_weights.append( record.weight )
        avg_strength = sum( record_weights ) / len( record_weights )
    except:
        fav_cat,workout_per_week,avg_strength = '','',''

    return fav_cat,workout_per_week,avg_strength
# 3fef7ff0fc1660c6bd319b3a8109fcb9f81985eabcbbf8958869ef03d605a9eb