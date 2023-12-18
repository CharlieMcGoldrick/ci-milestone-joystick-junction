from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
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
                return redirect('home')
        elif 'signup' in request.POST:
            if signup_form.is_valid():
                user = signup_form.save()
                
                # Get or create the group
                group, created = Group.objects.get_or_create(name='BasicUser')
                group.user_set.add(user)

                return redirect('account_management')
            else:
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


def logout_view(request):
    logout(request)
    return redirect('home')


# Error views
def custom_error_404(request, exception):
    return render(request, '404.html', {}, status=404)

def custom_error_500(request):
    return render(request, '500.html', {}, status=500)

def custom_error_403(request, exception):
    return render(request, '403.html', {}, status=403) 