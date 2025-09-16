from django.urls import path
from .views import *


urlpatterns = [
    path('rooms/', ChatRoomListCreateView.as_view(), name='chatroom-list-create'),
    path('rooms/<int:room_id>/messages/', RoomMessagesListCreateView.as_view(), name='room-messages'),
]