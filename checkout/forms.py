from django import forms


from .models import Order


class OrderForm(forms.ModelForm):
    """ Form for the user to fill in their shipping details """

    save_address = forms.BooleanField(
        required=False,
        label='Save to your profile',
        widget=forms.CheckboxInput(
            attrs={'style': 'width: 20px; height: 20px;'})
    )

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'phone_number',
                  'town_city', 'county', 'street_address', 'postcode',
                  'country',)
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'town_city': 'Town or City',
            'county': 'County/State',
            'street_address': 'Street Address',
            'postcode': 'Postal Code',
            'country': 'Country',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'first_name': 'e.g. John',
            'last_name': 'e.g. Doe',
            'email': 'example@domain.com',
            'phone_number': '+44 1234 567890',
            'town_city': 'Town or City',
            'street_address': 'Apt or house num. and street',
            'postcode': 'e.g. SW1A 1AA',
            'county': 'County, State or Locality',
        }

        for field in self.fields:
            if field != 'country' and field != 'save_address':
                placeholder = placeholders[field]

            self.fields[field].widget.attrs['placeholder'] = placeholder
            if field != 'save_address':
                self.fields[field].widget.attrs['class'] = (
                    'form-control form-control-lg'
                )
