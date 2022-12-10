from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User, Profile


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about_me', 'tags']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
