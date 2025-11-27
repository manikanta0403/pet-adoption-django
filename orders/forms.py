from django import forms
from django.core.validators import RegexValidator


phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)


class CheckoutForm(forms.Form):
    """Checkout form"""
    
    shipping_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    shipping_phone = forms.CharField(validators=[phone_regex], max_length=17, widget=forms.TextInput(attrs={'class': 'form-control'}))
    shipping_address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    shipping_city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    shipping_state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    shipping_zip_code = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))

