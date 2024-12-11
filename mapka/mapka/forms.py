from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserInfo



class RegisterForm(UserCreationForm):
    wojewodztwo = forms.ChoiceField(choices=UserInfo.WOJEWODZTWO_CHOICES, required=True)
    plec = forms.ChoiceField(choices=UserInfo.PLEC_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'wojewodztwo', 'plec']

class EditUserInfoForm(forms.ModelForm):
    wojewodztwo = forms.ChoiceField(choices=UserInfo.WOJEWODZTWO_CHOICES, required=True)
    plec = forms.ChoiceField(choices=UserInfo.PLEC_CHOICES, required=True)

    class Meta:
        model = UserInfo
        fields = ['wojewodztwo', 'plec']

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']