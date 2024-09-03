from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class CommercialConstant(models.Model):
    """
    A model for storing commercial constants related to delivery,
    promotions, tax rate, etc.
    """

    CONSTANT_TYPES = [
        ('int', 'Integer'),
        ('str', 'String'),
        ('float', 'Float'),
    ]

    name = models.CharField(max_length=50, unique=True)
    friendly_name = models.CharField(max_length=150, blank=True, null=True)
    value = models.CharField(max_length=255)
    constant_type = models.CharField(max_length=5, choices=CONSTANT_TYPES)
    description = models.TextField(blank=True, null=True)  # Friendly name

    def __str__(self):
        # Use description as a friendly name in string representation
        return f"{self.description or self.name}: {self.value}"

    # Getting the value of the constant by its name in appropriate type
    def get_value(self):
        if self.constant_type == 'int':
            return int(self.value)
        elif self.constant_type == 'float':
            return float(self.value) / 100
        return self.value


class PromoCodeUsage(models.Model):
    """
    Used for tracking promo code usage by users to prevent from misuse
    and to track the usage statistics
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    promo_code = models.CharField(max_length=50)
    used_at = models.DateTimeField(auto_now_add=True)
