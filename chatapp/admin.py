from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(RoomMessages)
admin.site.register(ChatRoom)

# Register your models here.
