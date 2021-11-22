from django import forms
from .models import Normal


class NormalForm(forms.ModelForm):
    class Meta:
        model = Normal
        fields = ['title','content']