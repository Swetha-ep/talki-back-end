from rest_framework import serializers
from .models import *

class CreateOrderSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    currency = serializers.CharField()

class TransactionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        # fields = ['payment_id','order_id','signature','amount', 'user']
        fields = '__all__'


class PaymentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ["name", "price", "duration" ]