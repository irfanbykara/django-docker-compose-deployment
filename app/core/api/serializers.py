from rest_framework.serializers import ModelSerializer
from ..models import Workout,User,Profile,Excercise


class WorkoutSerializers(ModelSerializer):
    class Meta:
        model = Workout
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ExcerciseSerializer(ModelSerializer):
    class Meta:
        model = Excercise
        fields = '__all__'