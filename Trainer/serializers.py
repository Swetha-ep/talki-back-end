from rest_framework import serializers
from .models import *

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        exclude = ('sender','recipient',)