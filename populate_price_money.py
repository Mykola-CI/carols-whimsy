import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carols_project.settings')
django.setup()

from djmoney.money import Money
from products.models import Product


def populate_price_money():
    for product in Product.objects.all():
        product.price_money = Money(product.price, 'GBP')
        product.save()


if __name__ == "__main__":
    populate_price_money()
    print("Price money field populated successfully.")
