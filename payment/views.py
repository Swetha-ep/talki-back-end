from django.shortcuts import get_object_or_404, render
from django.views import View
from .import client
from rest_framework.serializers import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import razorpay
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
# Create your views here.

class TransactionViewset(ModelViewSet):
    serializer_class = TransactionModelSerializer
    queryset = Transaction.objects.all()


class RazorpayClient:

    def create_order(self,amount,currency):
        data = {
            "amount" : amount * 100,
            "currency" : currency,
        }
        try:
            order_data = client.order.create(data=data)
            return order_data
        except Exception as e:
            raise ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : e
                }
            )
    
    def verify_payment(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        try:
            return client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
        except Exception as e:
            raise ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : e
                }
            )


rz_client = RazorpayClient


class CreateOrderAPIView(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        create_order_serializer = CreateOrderSerializer(data=request.data)
        if create_order_serializer.is_valid():
            rz_client_instance = RazorpayClient()  
            order_response = rz_client_instance.create_order(
                amount=create_order_serializer.validated_data.get("amount"),
                currency=create_order_serializer.validated_data.get("currency")
            )
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "order created",
                "data": order_response
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": create_order_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        



@api_view(['POST'])
def TransactionAPIView(request,user_id):
    print(request)
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        transaction_serializer = TransactionModelSerializer(data=request.data)
        print(user_id,'daxooooooo')
        print(transaction_serializer)
        if transaction_serializer.is_valid():
            
            rz_client = razorpay.Client(auth=("rzp_test_BYEW8iXywrLllV", "1Q3UJAXfMt4vxU6Az9PlrjdY"))

            
            try:
                rz_client.utility.verify_payment_signature({
                    "razorpay_signature": transaction_serializer.validated_data.get("signature"),
                    "razorpay_payment_id": transaction_serializer.validated_data.get("payment_id"),
                    "razorpay_order_id": transaction_serializer.validated_data.get("order_id"),
                })
            except Exception as e:
                return JsonResponse({
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

            # Save the transaction and update user status
            transaction_serializer.save(user=user)
            user.is_vip = True
            user.save()

            return JsonResponse({
                "status_code": status.HTTP_201_CREATED,
                "message": "transaction created"
            }, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": transaction_serializer.errors
            }
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)



class PaymentDetails(generics.RetrieveUpdateAPIView):
    # queryset= Payment.objects.all()
    serializer_class = PaymentModelSerializer
    def get_object(self):
        return Payment.objects.first()
    