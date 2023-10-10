from django.db import models
from Accounts.models import *


class Trainer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    TutorApplication = models.ForeignKey(TutorApplication,on_delete=models.CASCADE)
    is_online =  models.BooleanField(default=False)
    is_Tvip = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username