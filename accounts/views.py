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
class ProfileView(generics.ListAPIView):
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAdminUser]

    queryset = User.objects.all()
