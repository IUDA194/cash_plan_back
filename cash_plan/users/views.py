
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django_ratelimit.decorators import ratelimit

from rest_framework import generics, permissions, response, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Currency
from users.serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer

class UserRegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    @method_decorator(ratelimit(key='ip', rate='3/m', block=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save()

class UserLoginView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    
    @method_decorator(ratelimit(key='ip', rate='5/m', block=True))
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Log in the user
        login(request, user)
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'detail': 'Successfully logged in.',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
