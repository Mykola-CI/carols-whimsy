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
        max_length=255, null=True, blank=True)
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

    def get_title_readable(self):
        """Returns the human-readable name for the title."""
        title_display_map = dict(self.TITLE_CHOICES)
        return title_display_map.get(self.profile_title, '')


class ShippingAddress(models.Model):
    """ A user shipping address model for maintaining default"""

    user_profile = models.ForeignKey(
        UserProfile, related_name='addresses', on_delete=models.CASCADE)
    delivery_first_name = models.CharField(max_length=50)
    delivery_last_name = models.CharField(max_length=50)
    delivery_phone_number = models.CharField(max_length=20)
    delivery_email = models.EmailField(max_length=254)
    shipping_street_address = models.CharField(max_length=255)
    shipping_town_city = models.CharField(max_length=40)
    shipping_county = models.CharField(max_length=80)
    shipping_postcode = models.CharField(max_length=20)
    shipping_country = CountryField(blank_label='Country')
    shipping_is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.user_profile.user.username

    def save(self, *args, **kwargs):
        """ Override save method to set default shipping address
        to ensure there is only one default address per user"""

        if (
            not self.pk
                and ShippingAddress.objects.filter(
                    user_profile=self.user_profile).count() == 0):
            self.shipping_is_default = True
        elif self.shipping_is_default:
            # Set all other addresses for this user to non-default
            ShippingAddress.objects.filter(
                user_profile=self.user_profile, shipping_is_default=True
            ).update(shipping_is_default=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """ Override delete method to set default shipping address"""

        super().delete(*args, **kwargs)
        # After deletion, if there's only one address left, set it as default
        remaining_addresses = ShippingAddress.objects.filter(
            user_profile=self.user_profile)
        if remaining_addresses.count() == 1:
            remaining_address = remaining_addresses.first()
            remaining_address.shipping_is_default = True
            remaining_address.save()

    class Meta:
        verbose_name_plural = 'Shipping Addresses'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just saving the profile
    instance.userprofile.save()
