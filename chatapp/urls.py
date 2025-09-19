from django.urls import path
from .views import *


urlpatterns = [
    path("user/me/", CurrentUserView.as_view(), name="current_user"),

    path('rooms/', ChatRoomListCreateView.as_view(), name='chatroom-list-create'),
    path('rooms/<int:room_id>/messages/', RoomMessagesListCreateView.as_view(), name='room-messages'),
]