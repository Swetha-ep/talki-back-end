from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from Accounts.models import *

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['role'] = user.user_role
        token['is_staff'] = True
        return token
    

class UsersListSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class ApplicationListSerializer(ModelSerializer):
    class Meta:
        model = TutorApplication
