from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal, ROUND_HALF_UP
from djmoney.models.fields import MoneyField


class Brand(models.Model):
    ''' To store the brand names for the store's portfolio'''

    name = models.CharField(max_length=255, unique=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    '''Store the categories / types of products for the store's portfolio'''

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255, unique=False)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Theme(models.Model):
    '''Store the themes products relate to for the store's portfolio'''

    name = models.CharField(max_length=255, unique=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Season(models.Model):
    ''' Store seasons and occasions like Christmas, Easter, etc. '''

    name = models.CharField(max_length=255, unique=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True, blank=False)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, default=1,
        related_name='branded_products')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='group_of_products')
    theme = models.ForeignKey(
        Theme, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='theme_products')
    season = models.ForeignKey(
        Season, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='season_products')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price_money = MoneyField(
        max_digits=10, decimal_places=2, default_currency='GBP', null=True)  # Temporary field
    promo_text = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    material = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    other_details = models.TextField(blank=True, null=True)
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    image = models.ImageField(upload_to='', blank=True, null=True)
    image_url = models.URLField(max_length=1024, blank=True, null=True)

    # New fields to control stocks (21/10/24)
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Stock must be a non-negative integer."
    )

    # Define choices for preorder_status
    NOT_AVAILABLE = 1
    AVAILABLE = 2
    PRE_ORDER = 3

    PREORDER_STATUS_CHOICES = [
        (NOT_AVAILABLE, 'not available'),
        (AVAILABLE, 'available'),
        (PRE_ORDER, 'pre-order'),
    ]

    # Define the preorder_status field
    preorder_status = models.IntegerField(
        choices=PREORDER_STATUS_CHOICES,
        default=NOT_AVAILABLE,
        help_text="Preorder status based on stock availability."
    )

    def save(self, *args, **kwargs):
        # Only override if not set to pre-order
        if self.preorder_status != self.PRE_ORDER:
            if self.stock == 0:
                self.preorder_status = self.NOT_AVAILABLE
            else:
                self.preorder_status = self.AVAILABLE

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_discounted_price(self):
        """
        Returns the price after applying the discount.
        """
        discounted_price = self.price * (1 - self.discount)

        # Round to 2 decimal places
        rounded_price = Decimal(discounted_price).quantize(
            Decimal('0.00'), rounding=ROUND_HALF_UP)

        return rounded_price
