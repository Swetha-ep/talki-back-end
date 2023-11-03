from django.urls import path
# from .serializers import CreateOrderSerializer
from .views import *
from .import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('transaction', views.TransactionViewset, basename='transaction_view')

urlpatterns = [
    path("order/create/<int:user_id>/",CreateOrderAPIView.as_view(), name="create-order-api"),
    path("order/complete/<int:user_id>/",views.TransactionAPIView, name="complete-order-api"),
    path("paymentdetails/",PaymentDetails.as_view(), name="payment-details"),

]

urlpatterns += router.urls