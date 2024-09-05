from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Wishlist


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just saving the profile
    instance.userprofile.save()


@receiver(post_save, sender=User)
def create_user_wishlist(sender, instance, created, **kwargs):
    """
    Create a wishlist for the new user
    """
    if created:
        Wishlist.objects.create(user=instance)
