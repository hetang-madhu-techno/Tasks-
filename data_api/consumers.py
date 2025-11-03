import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TopicConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("topics_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("topics_group", self.channel_name)

    async def receive(self, text_data):
        # Not used for now — could handle user messages later
        pass

    async def send_new_topic(self, event):
        await self.send(text_data=json.dumps({
            "title": event["title"],
            "user": event["user"]
        }))
    async def send_deleted_topic(self, event):
        await self.send(text_data=json.dumps({
            "deleted_id": event["id"]
        }))
