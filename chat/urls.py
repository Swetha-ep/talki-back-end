from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("user-previous-chats/<int:request_id>/", PreviousMessagesView.as_view()),
    path("get-into-chat/<int:user_id>/<int:trainer_id>/", GetIntoChat.as_view())
]
