from django import views
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
 
urlpatterns = [
   path('login',AdminTokenObtainPairView.as_view(), name='AdminTokenObtainPairView'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   path('userslist/',UsersList.as_view(), name="UsersList"),
   path('user-block/<int:pk>/', UserBlockView.as_view(), name='user-block'),
   path('user-unblock/<int:pk>/', UserUnblockView.as_view(), name='user-unblock'),

   path('applicationlist/',ApplicationList.as_view(), name="ApplicationList"),
   path('application-detail/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
   path('accept_application/<int:application_id>/', views.accept_application, name='accept_application'),
   path('decline_application/<int:application_id>/', views.decline_application, name='decline_application'),
   
   path('trainers/', TrainerListView.as_view(), name='trainer-list'),
   path('user-application/<int:user_id>/', UserApplicationView.as_view(), name='user-application-detail'),

   path('trainer-vip/<int:pk>/',TrainerVipView.as_view(),name="trainer-vip"),
   path('trainer-nonvip/<int:pk>/',TrainerNonVipView.as_view(),name="trainer-nonvip"),
   path('trainer-block/<int:pk>/',TrainerBlockView.as_view(), name="trainer-block"),
   path('trainer-unblock/<int:pk>/',TrainerUnblockView.as_view(), name="trainer-unblock"),
   path('trainer-online/',TrainerOnlineListView.as_view(),name="trainer-online"),
   path('user-status/', views.user_status, name='user-status'),
   path('trainer-status/', views.trainer_status, name='trainer-status'),

]
