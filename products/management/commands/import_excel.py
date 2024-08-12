import os
import pandas as pd
from django.core.management.base import BaseCommand

from products.models import Product, Category, Theme, Season, Brand


class Command(BaseCommand):
    help = 'Import data from an Excel file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path', type=str, help='The path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        # Resolve the absolute path
        file_path = os.path.abspath(file_path)

        # Check if the file exists
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR('File does not exist'))
            return

        # Read the Excel file
        df = pd.read_excel(file_path)

        # Define the column mapping dictionary
        COLUMN_MAPPING = {
            'name': 'name',
            'sku': 'sku',
            'brand_id': 'brand_id',
            'category_id': 'category_id',
            'theme_id': 'theme_id',
            'season_id': 'season_id',
            'price': 'price',
            'promo_text': 'promo_text',
            'size': 'size',
            'material': 'material',
            'color': 'color',
            'other_details': 'other_details',
            'discount': 'discount',
            "image": "image"
        }

        # Rename columns based on the mapping dictionary
        df.rename(columns=COLUMN_MAPPING, inplace=True)

        # Create model instances
        for _, row in df.iterrows():
            try:
                brand = Brand.objects.get(id=row['brand_id'])
                category = Category.objects.get(id=row['category_id'])
                theme = Theme.objects.get(id=row['theme_id'])
                season = Season.objects.get(id=row['season_id'])
                Product.objects.create(
                    name=row['name'],
                    sku=row['sku'],
                    brand=brand,
                    category=category,
                    theme=theme,
                    season=season,
                    price=row['price'],
                    promo_text=row['promo_text'],
                    size=row['size'],
                    material=row['material'],
                    color=row['color'],
                    other_details=row['other_details'],
                    discount=row['discount'],
                    image=row['image']
                )
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f'Category with ID {row["category"]} does not exist'))
                continue

        self.stdout.write(self.style.SUCCESS(
            'Successfully imported data from Excel'))
