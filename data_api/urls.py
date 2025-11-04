from django.urls import path
from .views import TopicListCreateView , RetrieveUpdateDestroyTopicView, trigger_task

urlpatterns = [
    path('topics/', TopicListCreateView.as_view(), name='topic-list-create'),
    path('topics/<int:pk>/', RetrieveUpdateDestroyTopicView.as_view(), name='topic-detail'),
    path('run-task/', trigger_task, name='run_task'),
]
