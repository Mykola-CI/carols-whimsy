from djmoney.contrib.exchange.models import convert_money


def convert_price(price, target_currency):
    # If the price is already in the target currency, return it as is
    if price.currency == target_currency:
        return price

    # Convert from GBP to USD first, since rates are fetched with USD as base
    if price.currency == 'GBP':
        # Convert GBP to USD
        usd_price = convert_money(price, 'USD')
        # Convert USD to the target currency
        return convert_money(usd_price, target_currency)

    # If the price is not in GBP and not in the target currency,
    # directly convert it using available rates
    return convert_money(price, target_currency)
