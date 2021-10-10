from django.forms import ModelForm
from django import forms


class TestForm(forms.Form):
    input = forms.CharField(max_length=100, required=False)
