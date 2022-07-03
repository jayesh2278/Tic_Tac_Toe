from channels.consumer import AsyncConsumer,SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

from time import sleep
import json


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        #this group name data send from url so splite url and get group name by using scope
        #group_name = self.scope['url_route']['kwargs']['groupname']
        
        async_to_sync( self.channel_layer.group_add)('programer',self.channel_name)
        
        self.send({
            "type" : "websocket.accept"
        })

    def websocket_receive(self,event):
            # for sending data to group
            async_to_sync( self.channel_layer.group_send)('programer',{
                 #  type is use for send data to client like self.send({****})
                 "type" : "chat.message",
                 'message' : event["text"]
             })

     # send data to client from server       
    def chat_message(self,event):
        
        self.send({
                 "type": "websocket.send",
                 "text" : event["message"]

             })    

    def websocket_disconnected(self,event):
        async_to_sync( self.channel_layer.group_discard)('programer',self.channel_name)
        raise StopConsumer()


















class   MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self,event):
        await self.send({
            "type" : "websocket.accept"
        })

    async def websocket_receive(self,event):
        print(event)
        await self.send({
                "type": "websocket.send",
                "text" : "message send to client from server"

            })

    async def websocket_desconnected(self,event): 
                raise StopConsumer()