from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


class UserProfile(models.Model):
    """ A user profile model for maintaining default"""

    TITLE_CHOICES = [
        ('None', 'Prefer not to use'),
        ('Mr', 'Mr.'),
        ('Mrs', 'Mrs.'),
        ('Ms', 'Ms.'),
        ('Miss', 'Miss'),
        ('Dr', 'Dr.'),
        ('Prof', 'Prof.'),
        ('Mx', 'Mx.'),
        ('Rev', 'Rev.'),
        ('Sir', 'Sir'),
        ('Dame', 'Dame'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_phone_number = models.CharField(
        max_length=20, null=True, blank=True)
    profile_street_address = models.CharField(
        max_length=80, null=True, blank=True)
    profile_town_city = models.CharField(max_length=40, null=True, blank=True)
    profile_county = models.CharField(max_length=80, null=True, blank=True)
    profile_postcode = models.CharField(max_length=20, null=True, blank=True)
    profile_country = CountryField(
        blank_label='Country', null=True, blank=True)
    profile_date_of_birth = models.DateField(null=True, blank=True)
    profile_title = models.CharField(
        max_length=5, choices=TITLE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def get_title_friendly_name(self):
        """Returns the human-readable name for the title."""
        title_display_map = dict(self.TITLE_CHOICES)
        return title_display_map.get(self.title, '')


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just saving the profile
    instance.userprofile.save()
