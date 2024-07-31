from django.db import models


class Brand(models.Model):
    ''' To store the brand names for the store's portfolio'''

    name = models.CharField(max_length=255, unique=True)
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
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='categories')

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, blank=True, null=True, related_name='theme_products')
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, blank=True, null=True, related_name='season_products')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    promo_text = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    material = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    other_details = models.TextField(blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.name
