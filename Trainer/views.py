from django.shortcuts import render
from requests import request
from rest_framework import generics,status
from Accounts.models import *
from Accounts.serializers import *
from .models import *
from Dashboard.models import *
from Dashboard.serializers import *
from .serializers import *
from django.http import Http404, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
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
    


# @api_view(['POST'])
# def RequestCreateView(request, sender_id, recipient_id):
#     try:
#         sender = User.objects.get(pk=sender_id)
#         recipient = User.objects.get(pk=recipient_id)
#     except User.DoesNotExist:
#         return Response({'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

#     if sender.is_vip:
#         request_instance = Requests.objects.create(sender=sender, recipient=recipient)
#         return Response({'message': 'Connection request sent successfully.'}, status=status.HTTP_201_CREATED)
#     else:
#         if recipient.is_Tvip:
#             return Response({'message': 'You are not a VIP user to connect this trainer.'}, status=status.HTTP_403_FORBIDDEN)
#         else:
#             request_instance = Requests.objects.create(sender=sender, recipient=recipient)
#             return Response({'message': 'Connection request sent successfully.'}, status=status.HTTP_201_CREATED)


