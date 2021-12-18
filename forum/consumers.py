import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone 

class ForumConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.course_forum_name = 'course_forum_%s' % self.id
        # join course forum
        await self.channel_layer.group_add(
            self.course_forum_name, self.channel_name)
        # Accept connection
        await self.accept()
    
    async def disconnect(self, close_code):
        # leanve course forum
        await self.channel_layer.group_discard(
            self.course_forum_name, self.channel_name)
        
    # receive message from webSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        # send message to course forum
        await self.channel_layer.group_send(
            self.course_forum_name, {'type':'chat_message', 
                                     'message':message,
                                     'user':self.user.username,
                                     'datetime':now.isoformat()}
        )
    
    # Receive message from course forum
    async def chat_message(self, event):
        # send message to Websocket
        await self.send(text_data=json.dumps(event))