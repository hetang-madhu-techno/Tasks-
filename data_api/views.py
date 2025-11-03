from rest_framework import generics , permissions
from .models import Topic
from .serializers import TopicSerializer
from rest_framework.exceptions import PermissionDenied

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



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
        
class RetrieveUpdateDestroyTopicView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def perform_destroy(self, instance):
        
        if not self.request.user.is_staff:
            raise PermissionDenied("Only admin users can delete topics.")
        instance.delete()
    


    
    