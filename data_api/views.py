from rest_framework import generics , permissions
from .models import Topic
from .serializers import TopicSerializer
from rest_framework.exceptions import PermissionDenied

from rest_framework.response import Response

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
import threading
from .tasks import background_task_example


def trigger_task(request):
    threading.Thread(target=background_task_example).start()
    return JsonResponse({"status": "Background task started"})

class TopicListCreateView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        topic = serializer.save(user=self.request.user)
        

        
        
        # Broadcast to WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "topics_group",
            {
                "type": "send_new_topic",
                "title": topic.title,
                "user": topic.user.username,
            }
        )
        return Response({"message": "Topic created successfully"})
        
class RetrieveUpdateDestroyTopicView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def perform_destroy(self, instance):
        
        user = self.request.user

        
        if user.is_superuser or user.is_staff:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "topics_group",
                {"type": "send_deleted_topic", "id": instance.pk},
            )
            instance.delete()
            return

        if instance.user == user:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "topics_group",
                {"type": "send_deleted_topic", "id": instance.pk},
            )
            instance.delete()
            return


        # Otherwise deny
        raise PermissionDenied("You do not have permission to delete this topic.")


    
    