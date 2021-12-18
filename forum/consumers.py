import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ForumConsumer(WebsocketConsumer):
    def connect(self):
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.course_forum_name = 'course_forum_%s' % self.id
        # join course forum
        async_to_sync(self.channel_layer.group_add)(
            self.course_forum_name, self.channel_name)
        # Accept connection
        self.accept()
    
    def disconnect(self, close_code):
        # leanve course forum
        async_to_sync(self.channel_layer.group_discard)(
            self.course_forum_name, self.channel_name)
        
    # receive message from webSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # send message to course forum
        async_to_sync(self.channel_layer.group_send)(
            self.course_forum_name, {'type':'chat_message', 'message':message}
        )
    
    # Receive message from course forum
    def chat_message(self, event):
        # send message to Websocket
        self.send(text_data=json.dumps(event))