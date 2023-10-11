from django.shortcuts import render
from rest_framework import generics,status
from Accounts.models import *
from Accounts.serializers import *
from Dashboard.models import *
from Dashboard.serializers import *
from django.http import Http404, JsonResponse
from rest_framework.response import Response
# Create your views here.


class TrainerOnlineView(generics.UpdateAPIView):
    queryset = User.objects.filter(user_role = 'trainer')
    serializer_class = UserRegistrationSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_online = True
        user.save()
        return Response({'message' : 'You are Online now !'}, status=status.HTTP_200_OK)
    

class TrainerOfflineView(generics.UpdateAPIView):
    queryset = User.objects.filter(user_role='trainer')
    serializer_class = UserRegistrationSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_online = False
        user.save()
        return Response({'message' : 'You are Offline now !'}, status=status.HTTP_200_OK)