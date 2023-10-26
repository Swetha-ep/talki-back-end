from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User , TutorApplication,Requests


admin.site.register(User)
admin.site.register(TutorApplication)
admin.site.register(Requests)


# class ChatMessagesAdmin(admin.ModelAdmin):
#     list_editable= ['is_read']
#     list_display=['sender' ,'reciever','message','is_read']

# admin.site.register(ChatMessages,ChatMessagesAdmin)