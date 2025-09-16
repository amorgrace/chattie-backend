from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()


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