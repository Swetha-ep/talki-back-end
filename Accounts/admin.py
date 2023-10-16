from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User , TutorApplication,Requests


admin.site.register(User)
admin.site.register(TutorApplication)
admin.site.register(Requests)
