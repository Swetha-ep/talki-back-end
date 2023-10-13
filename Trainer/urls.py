from django.urls import path
from .views import *
from .import views
from rest_framework_simplejwt.views import TokenRefreshView
 
urlpatterns = [
   path('trainer-online/<int:pk>/', TrainerOnlineView.as_view(), name='user-block'),
   path('trainer-offline/<int:pk>/', TrainerOfflineView.as_view(), name='user-block'),
   path('trainer-connect/<int:sender_id>/<int:recipient_id>/', views.RequestCreateView, name='trainer-connect'),

]
