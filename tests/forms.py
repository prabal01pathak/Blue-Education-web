from django.forms import ModelForm
from django import forms
from .models import Title,Questions,Math
from .models import exam_choice,subjects_choices


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

class FormFilter(forms.Form):
    exam_type = forms.ChoiceField(label="Select Exam Type",choices=exam_choice)
    class Meta:
        model = Title
        fields = ['exam_type']

class AddTitleForm(ModelForm):
    subjects = forms.MultipleChoiceField(choices=subjects_choices, widget=forms.CheckboxSelectMultiple) 
    class Meta:
        model = Title
        exclude = [None]
        

class AddQuestionForm(ModelForm):
    class Meta:
        model=Math
        exclude = ['paper_title']