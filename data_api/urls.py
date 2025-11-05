from django.urls import path
from .views import TopicListCreateView, RetrieveUpdateDestroyTopicView, DownloadCachedTopicsView

urlpatterns = [
    path('topics/', TopicListCreateView.as_view(), name='topic-list-create'),
    path('topics/<int:pk>/', RetrieveUpdateDestroyTopicView.as_view(), name='topic-detail'),
    path("download_cached_topics/", DownloadCachedTopicsView.as_view(), name="download_cached_topics"),
]
