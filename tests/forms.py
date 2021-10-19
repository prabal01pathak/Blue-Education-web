from django.forms import ModelForm
from django import forms


class TestForm(forms.Form):
    radioButton1 = forms.ChoiceField(
        choices=[('A', 'A')],
        widget=forms.RadioSelect,
        label='A. ',
        required=True,
    )
    radioButton2 = forms.ChoiceField(
        choices=[('B', 'B')],
        widget=forms.RadioSelect,
        label='B. ',
        required=True,
    )
    radioButton3 = forms.ChoiceField(
        choices=[('C', 'C')],
        widget=forms.RadioSelect,
        label='C. ',
        required=True,
    )
    radioButton4 = forms.ChoiceField(
        choices=[('D', 'D')],
        widget=forms.RadioSelect,
        label='D. ',
        required=True,
    )
