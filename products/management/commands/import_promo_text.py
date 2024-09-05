import os
import pandas as pd
from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Update promo_text for existing Products from an Excel file'

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

        # Iterate over each row in the DataFrame
        unmatched_skus = []
        for _, row in df.iterrows():
            sku = row['sku']
            promo_text = row['promo_text']

            try:
                # Try to get the Product instance by sku
                product = Product.objects.get(sku=sku)
                # Update the promo_text field
                product.promo_text = promo_text
                product.save()
            except Product.DoesNotExist:
                # Log the unmatched sku
                unmatched_skus.append(sku)

        # Output the unmatched skus
        if unmatched_skus:
            self.stdout.write(
                self.style.WARNING(
                    'The following SKUs could not be matched: ' +
                    ', '.join(unmatched_skus))
            )
        else:
            self.stdout.write(self.style.SUCCESS(
                'Successfully updated promo_text for all matched SKUs'))
