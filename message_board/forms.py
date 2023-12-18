from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        User = get_user_model()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Username does not exist")

        if not user.check_password(password):
            raise forms.ValidationError("Incorrect password")

        return cleaned_data

class SignupForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(min_length=3, max_length=20)
    password1 = forms.CharField(min_length=8, max_length=50)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if not re.search(r'\d', password) or not re.search(r'[!@#$%^&*]', password):
            raise forms.ValidationError("Password must contain at least one digit and one special character.")
        return password



