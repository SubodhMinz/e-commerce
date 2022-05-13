from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer

class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label='Password (again)', widget=forms.PasswordInput())
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {'email':'Email'}
        
class LoginFrom(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True}))
    password = forms.CharField(widget=forms.PasswordInput())

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_('Email'), max_length=254, widget=forms.EmailInput(attrs={'atocomplete':'email', 'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password'}), help_text=password_validation.password_validators_help_text_html)
    new_password2 = forms.CharField(label=_('Confirm New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password'}))

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'locality', 'city', 'zipcode', 'state')
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
        }