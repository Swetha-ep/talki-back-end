
from django.urls import path,include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView, UserRegister, Activate
from .import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/<str:uidb64>/<str:token>/', Activate.as_view(), name='activate'),
    path('register/', UserRegister.as_view(), name='user_register'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('auth/google/', views.google_oauth2_auth, name='google-oauth2-auth', kwargs={'backend': 'google-oauth2'}),
    path('users/', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
]

