from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .widgets import CustomClearableFileInput
from products.models import Product, Category, Brand, Theme, Season
from checkout.models import Order


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(
        label='Product Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        brands = Brand.objects.all()
        themes = Theme.objects.all()
        seasons = Season.objects.all()

        brand_friendly_names = [
            (b.id, b.friendly_name) for b in brands]
        theme_friendly_names = [
            (t.id, t.friendly_name) for t in themes]
        season_friendly_names = [
            (s.id, s.friendly_name) for s in seasons]
        category_friendly_names = [
            (c.id, c.friendly_name) for c in categories]

        self.fields['category'].choices = category_friendly_names
        self.fields['brand'].choices = brand_friendly_names
        self.fields['theme'].choices = theme_friendly_names
        self.fields['season'].choices = season_friendly_names

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-1 rounded text-secondary'


class OrderStatusForm(forms.ModelForm):
    """ Form for updating the status of an order """

    STATUS_CHOICES = [
        ('', 'Change status'),  # Default choice
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES, required=True,
        widget=forms.Select(attrs={'class': 'form-select m-0'}),
        label='')

    class Meta:
        model = Order
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super(OrderStatusForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('status', css_class='m-0')
        )
