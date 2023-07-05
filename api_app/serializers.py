from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import CustomUser, UserDetails


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'
