from rest_framework import serializers
from users.models import UserProfile, Barbers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class BarbersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barbers
        fields = '__all__'
