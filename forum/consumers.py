import json
from channels.generic.websocket import WebsocketConsumer

class ForumConsumer(WebsocketConsumer):
    def connect(self):
        # Accept connection
        self.accept()
    
    def disconnect(self, close_code):
        pass
    # receive message from webSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # send message to Websocket
        self.send(text_data=json.dumps({'message':message})) 