from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from Accounts.models import *
from Accounts.serializers import *
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.generics import *


class PreviousMessagesView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        request_id = int(self.kwargs["request_id"])
        queryset = Message.objects.filter(thread_name='chat_'+str(request_id))
        return queryset
    

class GetIntoChat(APIView):
    def get(self, request, user_id, trainer_id):
        req_obj = Requests.objects.filter(sender=user_id, recipient=trainer_id,status='accepted').first()
        if req_obj:
            data = {}
            user_detail = {}
            trainer_details = {}
            user_detail['name'] = req_obj.sender.username
            trainer_details['name'] = req_obj.recipient.username
            data['channel_name'] = req_obj.id
            data['user'] = user_detail
            data['trainer'] = trainer_details
            return Response(data=data)
        else:
            return Response(data={'message': 'not found'}, status=404)





