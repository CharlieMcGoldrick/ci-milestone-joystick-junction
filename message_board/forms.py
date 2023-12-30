from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re


class SignupForm(UserCreationForm):
    """
    SignupForm is a form for user registration. It extends UserCreationForm
    provided by Django. It includes fields for username, email, and password.
    """
    email = forms.EmailField()
    username = forms.CharField(min_length=3, max_length=20)
    password1 = forms.CharField(min_length=8, max_length=50)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        """
        Validate that the username is not already in use.
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        """
        Validate that the email is not already in use.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def clean_password1(self):
        """
        Validate that the password contains at least one digit and one special
        character.
        """
        password = self.cleaned_data.get('password1')
        if not re.search(r'\d', password) or not re.search(
                r'[!@#$%^&*]', password):
            raise forms.ValidationError(
                "Password must contain at least one "
                "digit and one special character."
            )
        return password
