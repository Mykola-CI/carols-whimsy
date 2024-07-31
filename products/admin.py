from django.contrib import admin

from .models import Brand, Category, Theme, Season, Product


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Theme)
admin.site.register(Season)
admin.site.register(Product)
