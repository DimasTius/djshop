from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phone_field import PhoneField
from .models import *


class RegisterOrLoginForm:
    username = forms.EmailField(label='Электронная почта')


class RegisterForm(forms.Form):
    username = forms.EmailField(label='Электронная почта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    name = forms.CharField(max_length=255, label='Имя')
    surname = forms.SlugField(max_length=255, label='Фамилия')
    phone = forms.CharField(max_length=20, required=False, label='Контактный номер')


class UserProfileForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20, required=False, label='Контактный номер')
    street = forms.CharField(max_length=100)
    flat = forms.CharField(max_length=100)

    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.street = self.cleaned_data['street']
        user.flat = self.cleaned_data['flat']
        user.save()



