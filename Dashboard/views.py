from rest_framework_simplejwt.views import TokenObtainPairView
from Accounts.serializers import *
from server import settings
from .serializers import *
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,UpdateAPIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import Http404, JsonResponse



class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer


# User List
class UsersList(ListAPIView):
    serializer_class = UsersListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email','username','user_role']
    pagination_class = PageNumberPagination
    queryset = User.objects.filter(user_role='user').exclude(is_staff=True).order_by('-id')


class UserBlockView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'message': 'User blocked successfully'}, status=status.HTTP_200_OK)


class UserUnblockView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'message': 'User unblocked successfully'}, status=status.HTTP_200_OK)
    



class ApplicationList(ListAPIView):
    serializer_class = TutorApplicationViewSerializer
    search_fields = ['name','phone','email']
    queryset = TutorApplication.objects.all()
    



class ApplicationDetailView(generics.RetrieveAPIView):
    queryset = TutorApplication.objects.all()
    serializer_class = TutorApplicationViewSerializer


   
@api_view(["POST"])
def accept_application(request, application_id):
    
    try:
        application = TutorApplication.objects.get(pk=application_id)
       
        application.status = 'accepted'
        application.save()

        user = application.user
        user.is_trainer = True
        user.user_role = 'trainer'
        user.save()

        subject = 'Application Accepted'
        message = 'Congratulations! You have been recruited for the post.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [application.user.email]

        html_message = render_to_string('user/accepted_email.html')  

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            html_message=html_message,
        )

        return JsonResponse({'message': 'Application accepted successfully'})
        
    except TutorApplication.DoesNotExist:
        return JsonResponse({'error': 'Application not found.'}, status=404)
    


@api_view(["POST"])
def decline_application(request, application_id):
    try:
        application = TutorApplication.objects.get(pk=application_id)
       
            
        application.status = 'declined'
        application.save()

        
        subject = 'Application Declined'
        message = 'We regret to inform you that your application has been declined.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [application.user.email]

        html_message = render_to_string('user/declined_email.html')  

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            html_message=html_message,
        )

        # Delete the application from the database
        application.delete()

        return JsonResponse({'message': 'Application declined successfully'})
        
    except TutorApplication.DoesNotExist:
        return JsonResponse({'error': 'Application not found.'}, status=404)
    

class TrainerListView(generics.ListAPIView):
    queryset = User.objects.filter(user_role='trainer')
    serializer_class = UsersListSerializer


class UserApplicationView(generics.RetrieveAPIView):
    serializer_class = TutorApplicationViewSerializer

    def get_object(self):
        user_id = self.kwargs.get('user_id')

        try:
            application = TutorApplication.objects.get(user_id=user_id)
            return application
        except TutorApplication.DoesNotExist:
            raise Http404("TutorApplication does not exist")



class TrainerVipView(generics.UpdateAPIView):
    queryset = User.objects.filter(user_role='trainer')
    serializer_class = UserRegistrationSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_Tvip = True
        user.save()
        return Response({'message' : 'Selected as VIP trainer'},status= status.HTTP_200_OK)
    

class TrainerNonVipView(generics.UpdateAPIView):
    queryset = User.objects.filter(user_role='trainer')
    serializer_class = UserRegistrationSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_Tvip = False
        user.save()
        return Response({'message' : 'Selected as non-VIP trainer'},status= status.HTTP_200_OK)



class TrainerBlockView(generics.UpdateAPIView):
    queryset = User.objects.filter(user_role='trainer')
    serializer_class = UserRegistrationSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_trainer = False
        user.save()
        return Response({'message': 'User blocked successfully'}, status=status.HTTP_200_OK)
    

class TrainerUnblockView(generics.UpdateAPIView):
    queryset = User.objects.filter(user_role = 'trainer')
    serializer_class = UserRegistrationSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_trainer = True
        user.save()
        return Response({'message': 'User unblocked successfully'}, status=status.HTTP_200_OK)