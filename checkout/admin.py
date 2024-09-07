from django.contrib import admin

from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('item_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'stripe_pid',)

    fields = ('order_number', 'date', 'first_name', 'last_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_city', 'street_address',
              'county', 'delivery_cost', 'order_total', 'grand_total',
              'user_profile', 'stripe_pid', 'status', 'shipping_address',
              'saving', 'original_cart',)

    list_display = ('order_number', 'date', 'user_profile', 'last_name',
                    'order_total', 'grand_total', 'status',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
