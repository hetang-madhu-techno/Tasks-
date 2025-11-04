import re
from urllib import request
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

# Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# Profile (for viewing user details)
class ProfileView(generics.RetrieveAPIView):
    """Return the currently authenticated user's profile.

    If you want an admin-only list of users, add a separate view.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    

    