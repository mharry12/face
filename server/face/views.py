from rest_framework import generics, permissions
from .models import FaceUser
from .serializers import FaceUserSerializer

class FaceUserListCreateView(generics.ListCreateAPIView):
    queryset = FaceUser.objects.all()
    serializer_class = FaceUserSerializer
    permission_classes = [permissions.AllowAny]  # No auth required
    authentication_classes = []  # Disable authentication
