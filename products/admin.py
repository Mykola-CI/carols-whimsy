from django.contrib import admin

from .models import Brand, Category, Theme, Season, Product


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'friendly_name', 'description')
    readonly_fields = ('id',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'friendly_name', 'description')
    readonly_fields = ('id',)


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'friendly_name', 'description')
    readonly_fields = ('id',)


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'friendly_name', 'description')
    readonly_fields = ('id',)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'sku', 'brand', 'category',
        'theme', 'season', 'price', 'stock', 'preorder_status', 'image')
    readonly_fields = ('id',)


admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Product, ProductAdmin)
