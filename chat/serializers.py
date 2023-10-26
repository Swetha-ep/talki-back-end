from .models import *
from rest_framework import serializers
from Accounts.serializers import *
from rest_framework.serializers import SerializerMethodField


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ["message", "sender"]


class MessageListSerializer(serializers.ModelSerializer):
    user_profile = SerializerMethodField
    username = SerializerMethodField

    class Meta:
        model = Message
        fields = ["user_profile", "username"]

    def get_username(self, obj):
        return obj

    def get_user_profile(self, obj):
        return UserEditSerializer(
            User.objects.filter(user__username=obj).first()
        ).data.get("profile_pic")
