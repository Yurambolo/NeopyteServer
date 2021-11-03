from django import forms
from .models import GENDER_CHOICES


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    company = forms.CharField(max_length=100, null=True)
    gender = forms.CharField(max_length=50, choices=GENDER_CHOICES, null=True)
