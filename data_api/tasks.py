from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time
from celery import shared_task

from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def remind_users_to_add_topic():
    print("⏰ Running reminder task...")

    channel_layer = get_channel_layer()

    for user in User.objects.filter(is_active=True):
        async_to_sync(channel_layer.group_send)(
            "topics_group",  # Same group used in consumers.py
            {
                "type": "send_notification",
                "message": f"Hey {user.username}! 🕐 Don’t forget to add a new topic!",
            }
        )

    print("✅ Reminder sent to all active users.")


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
