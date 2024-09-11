from django import forms


class PromoCodeForm(forms.Form):
    promo_code = forms.CharField(
        max_length=255,
        required=True,
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter promo code',
                'class': 'form-control form-control-lg',
            },
        )
    )
