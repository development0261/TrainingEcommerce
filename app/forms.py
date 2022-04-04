from dataclasses import field, fields
import email
from pyexpat import model
from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

from app.models import Customer


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email  = forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        labels = {'email':'Email'}
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','state','zipcode','phone']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
        'locality':forms.TextInput(attrs={'class':'form-control'}),
        'city':forms.TextInput(attrs={'class':'form-control'}),
        'state':forms.Select(attrs={'class':'form-control'}),
        'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
        'phone':forms.TextInput(attrs={'class':'form-control'})
        }

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=("Old Password"),strip=False,widget=forms.PasswordInput(attrs={
        'autocomplete':'current-password','autofocus':True,'class':'form-control'
    }))
    new_password1 = forms.CharField(label=("New Password"),strip=False,widget=forms.PasswordInput(attrs= {
        'autocomplete':'new-password','class':'form-control'
    }),
    help_text = password_validation.password_validators_help_text_html())

    new_password2 = forms.CharField(label=("Confirm New Password"),strip=False,widget=forms.PasswordInput(attrs=
    {'autocomplete':'new-password','class':'form-control'}))
   
     