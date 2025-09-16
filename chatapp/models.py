from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

User = settings.AUTH_USER_MODEL

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be registered")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

        

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=200)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

class ChatRoom(models.Model):
    room_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.room_name
    

class RoomMessages(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='room_messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} : {self.message}"
    
    class Meta:
        ordering = ['-created']