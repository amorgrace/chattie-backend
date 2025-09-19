from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from dj_rest_auth.views import APIView, LoginView, GenericAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

class AmorLoginView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = AmorLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid email or password."},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, user.password):
            return Response({"detail": "Invalid email or password."},
                            status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"key": token.key}, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name="dispatch")
class APITokenLogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.auth:
            request.auth.delete()
        return Response({"detail": "Logout Successful"}, status=status.HTTP_200_OK)

class CurrentUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ChatRoomListCreateView(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer


class RoomMessagesListCreateView(generics.ListCreateAPIView):
    serializer_class = RoomMessagesSerializer

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return RoomMessages.objects.filter(room_id=room_id)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, room_id = self.kwargs['room_id'])