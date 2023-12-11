from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import UserBase


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Your email', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        label='Enter username', min_length=4, max_length=50, help_text='Required'
    )
    email = forms.EmailField(label='Enter your email address', max_length=100, help_text='Required', error_messages={'required': 'Sorry, an email address is required to make an account.'})
    password = forms.CharField(label='Enter a password for your account', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Enter your chosen password again', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email')

    
    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Sorry, this username already exists.")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'This email already exists. Please use another email address.')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})

class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Account not found.')
        return email

class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Enter new password again', 'id': 'form-new-pass2'}))

class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Account username (can not be changed)', max_length=150, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'username', 'id': 'form-username', 'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='First name', min_length=2, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'First name', 'id': 'form-firstname'}))
    
    last_name = forms.CharField(
        label='Last name', min_length=2, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Last name', 'id': 'form-lastname'}))
    
    address_line_1 = forms.CharField(
        label='Address Line 1', max_length=150, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Address Line 1', 'id': 'form-address-line-1'}))
    
    address_line_2 = forms.CharField(
        label='Address Line 2', max_length=150, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Address Line 2', 'id': 'form-address-line-2'}))
    
    town_city = forms.CharField(
        label='Town/City', max_length=150, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Town/City', 'id': 'form-town-city'}))

    postcode = forms.CharField(
        label='Postcode', max_length=12, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Postcode', 'id': 'form-postcode'}))

    country = CountryField().formfield(initial='GB', label='Country', widget=CountrySelectWidget(
        attrs={'class': 'form-control', 'placeholder': 'Country', 'id': 'form-country'}
    ))

    class Meta:
        model = UserBase
        fields = ('email', 'user_name', 'first_name', 'last_name', 'address_line_1', 'address_line_2', 'town_city', 'postcode', 'country',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['address_line_1'].required = True
        self.fields['postcode'].required = True