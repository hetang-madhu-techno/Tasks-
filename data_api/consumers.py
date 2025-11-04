import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TopicConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("✅ WebSocket connected")
        await self.channel_layer.group_add("topics_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print("❌ WebSocket disconnected")
        await self.channel_layer.group_discard("topics_group", self.channel_name)

    async def receive(self, text_data):
        print("📩 Received from frontend:", text_data)

    async def send_new_topic(self, event):
        print("📢 Sending new topic event:", event)
        await self.send(text_data=json.dumps({
            "title": event["title"],
            "user": event["user"]
        }))

    async def send_deleted_topic(self, event):
        print("🗑️ Sending deleted topic event:", event)
        # send a consistent payload key expected by the frontend
        await self.send(text_data=json.dumps({
            "deleted_id": event["id"]
        }))
