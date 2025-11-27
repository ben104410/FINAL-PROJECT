from django.shortcuts import render
from rest_framework import generics, permissions
from .models import User
from .serializers import RegisterSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    """
    Endpoint for user registration.
    POST -> creates a new user using RegisterSerializer
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveAPIView):
    """
    Endpoint for retrieving the authenticated user's profile.
    GET -> returns request.user serialized with UserSerializer
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Create your views here.
