from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

gender = (('Male',"Male"),("Female","Female"),("Other","Other"))
class UserCreate(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    mobile_no = forms.CharField(max_length=14, required=False)
    Email = forms.EmailField(max_length=254, required=True)
    gender = forms.ChoiceField(choices=gender)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    accept_terms = forms.BooleanField(required=True)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Username already exists")

    def clean_password(self):
        password = self.cleaned_data['password']
        confirm_pass = self.data['confirm_password']
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        if password != confirm_pass:
            raise forms.ValidationError("Passwords do not match")
        return password
    def clean_accept_terms(self):
        accept_terms = self.cleaned_data['accept_terms']
        if accept_terms == False:
            raise forms.ValidationError("You must accept the terms and conditions")
        return accept_terms
    def clean_email(self):
        email = self.cleaned_data['Email']
        print(email)
        try:
            User.objects.get(email=email)
            print("user already exist")
        except User.DoesNotExist:
            print("user does not exist")
            return email
        raise forms.ValidationError("Email already exists")

    
class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_new_password(self):
        new_password = self.data['new_password']
        if len(new_password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        return new_password
    def clean_confirm_password(self):
        new_password = self.data['new_password']
        confirm_password = self.data['confirm_password']
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password

class UserProfile(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    mobile_no = forms.CharField(max_length=14, required=False)
    Email = forms.EmailField(max_length=254, required=True)
    gender = forms.ChoiceField(choices=gender,required=False)
    
class PasswordResetForm(forms.Form):
    OTP = forms.CharField(max_length=6,required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_new_password(self):
        new_password = self.data['new_password']
        if len(new_password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        return new_password
    def clean_confirm_password(self):
        new_password = self.data['new_password']
        confirm_password = self.data['confirm_password']
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password
