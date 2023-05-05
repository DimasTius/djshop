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



