from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


admin.site.register(User)
admin.site.register(TutorApplication)
admin.site.register(Requests)
admin.site.register(Rating)
