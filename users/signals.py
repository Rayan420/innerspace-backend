from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile, FriendshipRequest, Friendship

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance,
                                   name=f"{instance.first_name or ''} {instance.last_name or ''}".strip(),
                                   )

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    user_profile, created = UserProfile.objects.get_or_create(user=instance)
    if not created:
        user_profile.save()

@receiver(post_save, sender=FriendshipRequest)
def friendship_request_created(sender, instance, created, **kwargs):
    """
    Signal handler for when a FriendshipRequest is created.
    Perform actions when a new friendship request is sent.
    """
    if created:
        print(f"New Friendship Request: {instance.from_user} to {instance.to_user}")

@receiver(post_save, sender=FriendshipRequest)
def friendship_request_accepted(sender, instance, created, **kwargs):
    """
    Signal handler for when a FriendshipRequest is accepted.
    Perform actions when a friendship request is accepted.
    """
    if not created and instance.status == 'accepted':
        print(f"Friendship Request Accepted: {instance.from_user} and {instance.to_user}")
        # Create or update Friendship instance
        Friendship.objects.get_or_create(from_user=instance.from_user, to_user=instance.to_user, status='accepted')

@receiver(post_delete, sender=Friendship)
def friendship_deleted(sender, instance, **kwargs):
    """
    Signal handler for when a Friendship instance is deleted.
    Perform actions when a friendship is unfriended.
    """
    print(f"Friendship Deleted: {instance.from_user} and {instance.to_user}")
    # You can perform additional actions here, such as updating friends list, etc.



# {
#   "username": "example_user",
#   "email": "user@example.com",
#   "password": "secure_password"
# }
