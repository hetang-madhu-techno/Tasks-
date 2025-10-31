from rest_framework import serializers
from . models import Topic


class TopicSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username') 
    
    class Meta:
        model = Topic
        fields = '__all__'

