"""
Custom forms for user registration and authentication
"""
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class PhoneNumberRegistrationForm(forms.Form):
    """
    Registration form using phone number as primary identifier
    """
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number',
            'type': 'tel'
        })
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email (optional)'
        })
    )
    
    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a strong password'
        })
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        # Check if phone already exists
        if UserProfile.objects.filter(phone=phone).exists():
            raise forms.ValidationError('This phone number is already registered.')
        
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Email is optional, but if provided it must be unique
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        if len(password1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        
        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        
        return cleaned_data


class PhoneNumberLoginForm(forms.Form):
    """
    Login form using phone number
    """
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number',
            'type': 'tel',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
