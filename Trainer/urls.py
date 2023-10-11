from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
 
urlpatterns = [
   path('trainer-online/<int:pk>/', TrainerOnlineView.as_view(), name='user-block'),
   path('trainer-offline/<int:pk>/', TrainerOfflineView.as_view(), name='user-block'),

]
