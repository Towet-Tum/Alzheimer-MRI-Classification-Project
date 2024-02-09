from django import forms
from django.contrib.auth.models import User
from .models import Conctact


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "password")


class ContactForm(forms.ModelForm):
    class Meta:
        model = Conctact
        fields = ["full_name", "email", "tel", "subject", "message"]
