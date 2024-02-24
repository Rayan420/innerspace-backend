# serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserProfile, FriendshipRequest

class UserProfileSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'
        
    def get_profile_pic(self, obj):
        try:
            pic = obj.profile_pic
        except:
            pic = None
        return pic

class CurrentUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'profile', 'username', 'email', 'is_superuser', 'is_staff', 'is_active', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    user_id = serializers.UUIDField(format='hex')  # Convert UUID to string

    class Meta:
        model = User
        fields = ['user_id', 'profile', 'username', 'email', 'is_superuser', 'is_staff']

class UserSerializerWithToken(UserSerializer):
    access = serializers.SerializerMethodField(read_only=True)
    refresh = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        exclude = ['password']

    def get_access(self, obj):
        token = RefreshToken.for_user(obj)

        token['email'] = obj.email
        token['username'] = obj.username
        return str(token.access_token)

    def get_refresh(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token)

class FriendshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = '__all__'
