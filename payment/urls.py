from django.urls import path
# from .serializers import CreateOrderSerializer
from .views import *
from .import views
urlpatterns = [
    path("order/create/<int:user_id>/",CreateOrderAPIView.as_view(), name="create-order-api"),
    path("order/complete/<int:user_id>/",views.TransactionAPIView, name="complete-order-api"),

]
