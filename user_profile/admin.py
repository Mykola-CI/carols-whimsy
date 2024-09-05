from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, ShippingAddress, Wishlist


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


class ShippingAddressAdmin(admin.ModelAdmin):
    model = ShippingAddress
    verbose_name_plural = 'Shipping Addresses'

    list_display = (
        'id',
        'delivery_first_name',
        'delivery_last_name',
        'delivery_phone_number',
        'delivery_email',
        'shipping_street_address',
        'shipping_town_city',
        'shipping_county',
        'shipping_postcode',
        'shipping_country',
        'user_profile',
        'shipping_is_default',
    )


# Unregister the original User admin and register the new User admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(ShippingAddress, ShippingAddressAdmin)

admin.site.register(Wishlist)
