import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

# creating the user manager class
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise TypeError('Users should have a username')
        if not email:
            raise TypeError('Users should have an email address')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user_model = self.model
        user = user_model(username=username, email=email, **extra_fields)

        if user_model.objects.filter(email=user.email).exists():
            raise ValueError('Email is already in use')
        if user_model.objects.filter(username=user.username).exists():
            raise ValueError('Username is already in use')

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        if password is None or not password.strip():
            raise TypeError('Password should not be empty')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)




# Creating a custom user model with additional fields


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    


class FriendshipRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    request_id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='requests_sent')
    to_user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='requests_received')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"FriendshipRequest #{self.request_id} - {self.from_user.user.username} to {self.to_user.user.username}, Status: {self.status}"

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.URLField(max_length=255, blank=True, null=True)
    house_count = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    is_private = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    email_verified = models.BooleanField(default=False)

    friends = models.ManyToManyField('self', related_name='friend', blank=True, through=FriendshipRequest, symmetrical=False)
    
    def __str__(self):
        return str(self.user.username)

class Friendship(models.Model):
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='friendships_initiated')
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='friendships_received')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Friendship between {self.from_user.user.username} and {self.to_user.user.username}"