from rest_framework import serializers
from .models import User, TutorApplication
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password','user_level', ]
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        token['email'] = user.email
        token['username'] = user.username
        token['user_role'] = user.user_role
        token['is_vip'] = user.is_vip
        token['is_active'] = user.is_active
       
        return token
    



class TutorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorApplication
        fields = '__all__'


class TutorApplicationViewSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()
    class Meta:
        model = TutorApplication
        fields = '__all__'


        
