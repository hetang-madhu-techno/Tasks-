from importlib.metadata import requires
from django.db import models
from django.conf import settings

class Topic(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name='topics')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    documentation_url = models.URLField(max_length=500, blank=False, null=False)
    video_url = models.URLField(max_length=500, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title