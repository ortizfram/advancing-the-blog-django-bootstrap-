from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Name..'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email..'}))
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Address..'}))
    state = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'State..'}))
    country = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Country..'}))
    zipcode = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Zipcode..'}))
