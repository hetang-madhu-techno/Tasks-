# Django & DRF imports
from django.core.cache import cache
from django.conf import settings
from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
# Channels imports
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Local app imports
from .models import Topic
from .serializers import TopicSerializer
import json


class DownloadCachedTopicsView(APIView):
    def get(self, request):
        # Use the same cache key as the topic list. If cache is empty,
        # fall back to loading from DB so the download still works.
        cached_topics = cache.get("topics_list")
        if not cached_topics:
            queryset = Topic.objects.all()
            cached_topics = TopicSerializer(queryset, many=True).data
            # Populate cache for future requests (short TTL fallback)
            cache.set("topics_list", cached_topics, timeout=getattr(settings, "CACHE_TTL", 300))

        json_data = json.dumps(cached_topics, indent=2)
        response = HttpResponse(
            json_data,
            content_type="application/json",
        )
        response["Content-Disposition"] = 'attachment; filename="cached_topics.json"'
        return response

class TopicListCreateView(generics.ListCreateAPIView):
   
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_permissions(self):
        # Allow anyone to GET, require auth for POST
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        """
        List topics, using cache for performance.
        """
        topics = cache.get("topics_list")
        if not topics:
            print("\n🗄️ Cache miss — loading from DB\n")
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            topics = serializer.data
            cache.set("topics_list", topics, timeout=getattr(settings, "CACHE_TTL", 300))
        else:
            print("\n⚡ Cache hit — loaded from Redis\n")
        return Response(topics)

    def perform_create(self, serializer):
        """
        Create a new topic, clear and rebuild cache, notify via WebSocket.
        """
        topic = serializer.save(user=self.request.user)
        # Clear and rebuild cache
        cache.delete("topics_list")
        topics = TopicSerializer(Topic.objects.all(), many=True).data
        cache.set("topics_list", topics, timeout=getattr(settings, "CACHE_TTL", 300))
        # Broadcast WebSocket event
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "topics_group",
            {
                "type": "send_new_topic",
                "title": topic.title,
                "user": topic.user.username,
            }
        )
        return Response({"message": "Topic created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveUpdateDestroyTopicView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Admin can access all, user sees only own topics
        if user.is_staff:
            return Topic.objects.all()
        return Topic.objects.filter(user=user)

    def perform_destroy(self, instance):
        user = self.request.user

        # 🚫 Restrict deletion to owner or admin
        if not user.is_staff and instance.user != user:
            raise PermissionDenied("You can delete only your own topics.")

        instance_id = instance.pk
        instance.delete()

        # 🔁 Clear and rebuild cache
        cache.delete("topics_list")
        topics = TopicSerializer(Topic.objects.all(), many=True).data
        cache.set("topics_list", topics, timeout=300)

        # 📢 Notify via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "topics_group",
            {
                "type": "send_deleted_topic",
                "id": instance_id,
            }
        )
