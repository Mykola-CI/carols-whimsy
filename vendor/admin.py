from django.contrib import admin
from .models import CommercialConstant


@admin.register(CommercialConstant)
class CommercialConstantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'friendly_name', 'value', 'constant_type',
                    'description')
    search_fields = ('name',)
