from django.urls import path
from .views import TopicListCreateView , RetrieveUpdateDestroyTopicView

urlpatterns = [
    path('topics/', TopicListCreateView.as_view(), name='topic-list-create'),
    path('topics/<int:pk>/', RetrieveUpdateDestroyTopicView.as_view(), name='topic-detail'),
]
