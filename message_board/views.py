from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from django.http import JsonResponse
from django.contrib.auth.models import User
import json 

def home(request):
    template_name = "index.html"
    return render(request, template_name)


def account_management(request):
    login_form = LoginForm(request.POST or None)
    signup_form = SignupForm(request.POST or None)

    if request.method == 'POST':
        if 'login' in request.POST:
            if login_form.is_valid():
                # Log the user in and redirect to the home page
                return redirect('home')
        elif 'signup' in request.POST:
            if signup_form.is_valid():
                # Signup the user and reload the page
                signup_form.save()
                return redirect('account_management')
            else:
                # Return an error message
                return JsonResponse({'error': signup_form.errors}, status=400)

    return render(request, 'account_management.html', {'login_form': login_form, 'signup_form': signup_form})


def check_username_email(request):
    data = json.loads(request.body)
    username = data.get('username')
    email = data.get('email')

    data = {
        'username_taken': User.objects.filter(username=username).exists(),
        'email_taken': User.objects.filter(email=email).exists()
    }

    return JsonResponse(data)

