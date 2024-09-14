from django.contrib import admin
from .models import CommercialConstant, PromoCodeUsage


@admin.register(CommercialConstant)
class CommercialConstantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'friendly_name', 'value', 'constant_type',
                    'description')
    search_fields = ('name',)


@admin.register(PromoCodeUsage)
class PromoCodeUsageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'promo_code', 'used_at')
    search_fields = ('user', 'promo_code')
