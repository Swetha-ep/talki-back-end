from django.db import models

# Create your models here.
from django.db import models
from Accounts.models import *

# Create your models here.
class Message(models.Model):
    sender = models.CharField(null=True,max_length=200)
    message = models.TextField(null=True)
    thread_name = models.CharField(null=True, max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'({self.thread_name})'