from django.db import models
from Accounts.models import User
from django.utils import timezone


# Create your models here.


class Payment(models.Model):
    name = models.CharField(max_length=100, default='Classic')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    duration = models.IntegerField(default=30)

    def __str__(self) -> str:
        return str(self.id)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_instance = models.ForeignKey(Payment, on_delete=models.CASCADE, default=1)
    payment_id = models.CharField(max_length=100, verbose_name="Payment ID", null=True)
    order_id = models.CharField(max_length=100, verbose_name="Order ID")
    signature = models.CharField(max_length=200, verbose_name="Signature")
    amount = models.IntegerField(verbose_name="Amount")
    datetime = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.datetime)

    def save(self, *args, **kwargs):
        if not self.datetime:
            self.datetime = timezone.now()

        if self.payment_instance.duration:
            duration = self.payment_instance.duration if self.payment_instance.duration else 30
            self.expires = self.datetime + timezone.timedelta(days=duration)
        super(Transaction, self).save(*args, **kwargs)