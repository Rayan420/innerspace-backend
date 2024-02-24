from django.contrib import admin
from datetime import timedelta
from .models import UserProfile, FriendshipRequest, Friendship

class AdminUserProfile(admin.ModelAdmin):
    list_display = ('get_email', 'get_utc', 'email_verified')
    search_fields = ('user__email',)  # Assuming 'user' is a ForeignKey field in UserProfile pointing to User
    list_filter = ('email_verified',)

    def get_email(self, obj):
        return obj.user.email

    def get_utc(self, obj):
        return obj.user.date_joined + timedelta(minutes=330)

    get_utc.short_description = 'Created (UTC)'
    get_email.short_description = 'Email'

admin.site.register(UserProfile, AdminUserProfile)
admin.site.register(FriendshipRequest)
admin.site.register(Friendship)