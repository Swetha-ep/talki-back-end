
from django.urls import path,include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView, UserRegister, Activate, TutorApplicationCreateView
from .import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/<str:uidb64>/<str:token>/', Activate.as_view(), name='activate'),
    path('register/', UserRegister.as_view(), name='user_register'),
    path('forgotpassword/', ForgotPassword.as_view(),name = 'forgot-password'),
    path('reset_validate/<uidb64>/<token>/',views.reset_validate, name='reset_validate'),
    path('reset-password/<int:user_id>', ResetPassword.as_view()),

    path('auth/', include('social_django.urls', namespace='social')),
    path('auth/google/', views.google_oauth2_auth, name='google-oauth2-auth', kwargs={'backend': 'google-oauth2'}),

    path('user-profile/<int:pk>/', UserProfileDetail.as_view(), name='user-profile'),

    path('submit-application/', TutorApplicationCreateView.as_view(), name='submit-tutor-application'),
    path('viewapplication/<int:id>', TutorApplicationRetrieve.as_view(), name='TutorApplicationRetrieve'),

    path('trainer-connect/<int:sender_id>/<int:recipient_id>/', views.RequestCreateView, name='trainer-connect'),
    path('senders-for-recipient/<int:recipient_id>/', Senders.as_view(), name='senders-for-recipient'),
    path('check-request/<int:sender_id>/<int:recipient_id>/', CheckRequestView.as_view(), name='check-request'),
    path('withdraw-request/<int:sender_id>/<int:recipient_id>/', WithdrawRequestView.as_view(), name='withdraw-request'),
    path('get_recipient_ids/<int:sender_id>/', views.get_recipient_ids_for_sender, name='get_recipient_ids_for_sender'),
    path('get_recipient_ids/<int:sender_id>/', views.get_recipient_ids_for_sender, name='get_recipient_ids_for_sender'),

    path('accept-request/<int:sender_id>/<int:receiver_id>/', AcceptRequestView.as_view(), name='accept_request'),
    path('user-vip/<int:pk>/', UserVipDetail.as_view(), name='user-vip'),
    
    
    
]

