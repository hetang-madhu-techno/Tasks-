from rest_framework import generics , permissions
from .models import Topic
from .serializers import TopicSerializer
from rest_framework.exceptions import PermissionDenied


class TopicListCreateView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class RetrieveUpdateDestroyTopicView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def perform_destroy(self, instance):
        
        if not self.request.user.is_staff:
            raise PermissionDenied("Only admin users can delete topics.")
        instance.delete()
    


    
    