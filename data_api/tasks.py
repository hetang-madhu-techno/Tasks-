from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time

from celery import shared_task


@shared_task
def notify_new_topic(topic_id, topic_title):
    print(f"⏳ Sending notification for topic {topic_title} (id={topic_id})...")
    time.sleep(5)  # Simulate delay
    print(f"✅ Notification sent for topic: {topic_title}")


def background_task_example():
    """Simple background function to simulate a long process"""
    print("Background task started...")
    time.sleep(5)  # simulate a long process (5 sec)
    print("Background task finished ✅")

    # Send message to WebSocket clients after it’s done
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "topics_group",
        {
            "type": "send_new_topic",
            "title": "✅ Background task completed",
            "user": "System"
        }
    )
