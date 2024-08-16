from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'phone_number',
                  'town_city', 'county', 'street_address', 'postcode',
                  'country',)
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            Field('email'),
            Field('phone_number'),
            Field('town_city'),
            Field('county'),
            Field('street_address'),
            Field('postcode'),
            Field('country'),
        )

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-lg'
            self.fields[field].label = False
