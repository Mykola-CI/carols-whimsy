from django.core.management.base import BaseCommand
from djmoney.contrib.exchange.models import Rate


class Command(BaseCommand):
    help = 'Adjust exchange rates to use GBP as the base currency'

    def handle(self, *args, **kwargs):
        try:
            # Get USD -> GBP rate
            usd_to_gbp_rate = Rate.objects.get(currency="GBP").value

            # Adjust all other rates relative to GBP
            for rate in Rate.objects.exclude(currency="GBP"):
                original_value = rate.value
                rate.value /= usd_to_gbp_rate
                rate.save()
                self.stdout.write(self.style.SUCCESS(
                    f'Adjusted {rate.currency}: {original_value} -> {rate.value}'
                ))

            self.stdout.write(self.style.SUCCESS(
                'All rates adjusted to GBP base currency successfully.'))
        except Rate.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                'GBP rate not found. Please ensure rates are updated first.'))
