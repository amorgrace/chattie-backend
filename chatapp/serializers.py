from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from .models import *

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class AmorLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    

class UserSerializer(serializers.ModelSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = ("username", "email",
                  "phone_number")
class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['room_name']


class RoomMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMessages
        fields = ['id', 'room', 'user', 'message', 'created']