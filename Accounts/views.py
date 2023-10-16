from urllib.parse import urlencode
from django.shortcuts import render
from .serializers import *
from .models import LEVEL_CHOICES, Requests, User
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User,TutorApplication
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.shortcuts import redirect
from social_django.utils import psa
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from decouple import config
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework import generics
from rest_framework.exceptions import NotFound

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserRegister(CreateAPIView):
    def get_serializer_class(self):
        return UserRegistrationSerializer  

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.user_role = "user"
            user.set_password(password)
            user.email = email
            user.save()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            token_bytes = urlsafe_base64_encode(force_bytes(token))
            activation_url = reverse('activate', args=[uidb64, token])
            current_site = Site.objects.get_current()
            backendurl = config('backendUrl')
            current_site.domain = backendurl
            current_site.save()
            mail_subject = 'Activate your account'
            message = render_to_string(
                'user/activation_email.html',
                {
                    'user': user,
                    'activation_url': activation_url,
                    'domain': current_site,
                    'uidb64': uidb64,
                    'token': token,
                }
            )
            from_email = settings.EMAIL_HOST_USER  # Make sure EMAIL_HOST_USER is properly configured in your settings
            to_email = email
            send_mail(mail_subject, message, from_email, [to_email])
            return Response({'message': 'Registration successful. Please check your email for activation instructions.'}, status=status.HTTP_201_CREATED)
        
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class Activate(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
            if user is not None and default_token_generator.check_token(user, token):
                    user.is_active = True
                    user.save()
                    message = 'Congrats! Account activated!'

                    
                    redirect_url = f'http://localhost:3000/login/?{urlencode({"message": message})}'
                    
            else:
                message = 'Invalid activation link'
                redirect_url = f'http://localhost:3000/login/?{urlencode({"message": message})}'

            return HttpResponseRedirect(redirect_url)
        
        except Exception as e:
            return Response({'message': 'Activation Failed'}, status=status.HTTP_400_BAD_REQUEST)


@psa('social:begin', 'social:complete')
def google_oauth2_auth(request, backend):
    return redirect('social:begin', backend=backend)



class UserProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserEditSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)      
        data = serializer.data
        data["level_choices"] = [{"label": choice[1]} for choice in LEVEL_CHOICES]

        return Response(data)
    
 

class TutorApplicationCreateView(CreateAPIView):
    serializer_class = TutorApplicationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data.get('user')

            existing_application = TutorApplication.objects.filter(user_id=user).first()
            
            if existing_application:
                return Response({'error': 'Tutor application already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'message': 'Tutor application submitted successfully.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class TutorApplicationRetrieve(ListAPIView):
    serializer_class = TutorApplicationViewSerializer

    def get_queryset(self):
        user_id = self.kwargs['id']
        queryset = TutorApplication.objects.filter(user_id=user_id)
        return queryset




@api_view(['POST'])
def RequestCreateView(request, sender_id, recipient_id):
    try:
        sender = User.objects.get(pk=sender_id)
        recipient = User.objects.get(pk=recipient_id)
    except User.DoesNotExist:
        return Response({'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    if sender.is_vip:
        request_instance = Requests.objects.create(sender=sender, recipient=recipient)
        return Response({'message': 'Connection request sent successfully.'}, status=status.HTTP_201_CREATED)
    else:
        if recipient.is_Tvip:
            return Response({'message': 'You are not a VIP user to connect this trainer.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            request_instance = Requests.objects.create(sender=sender, recipient=recipient)
            return Response({'message': 'Connection request sent successfully.'}, status=status.HTTP_201_CREATED)



class Senders(ListAPIView):
    def get_queryset(self):
        recipient_id = self.kwargs['recipient_id']
        try:
            recipient = User.objects.get(pk=recipient_id)
        except User.DoesNotExist:
            return []
        return Requests.objects.filter(recipient = recipient)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({'message' : 'Trainer does not exist'})
        
        senders = [request.sender for request in queryset]
        sender_data = UserEditSerializer(senders,many=True)

        return Response({'senders': sender_data.data})
    
