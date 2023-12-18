from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm 

def home(request):
    template_name = "index.html"
    return render(request, template_name)


def account_management(request):
    login_form = LoginForm(request.POST or None)
    signup_form = SignupForm(request.POST or None)

    if request.method == 'POST':
        print("POST request received")  # Debugging print statement
        if 'login' in request.POST:
            print("Login form submitted")  # Debugging print statement
            if login_form.is_valid():
                # Log the user in and redirect to the home page
                return redirect('home')
            else:
                print(login_form.errors)
        elif 'register' in request.POST:
            print("Signup form submitted")  # Debugging print statement
            if signup_form.is_valid():
                # Register the user and reload the page
                signup_form.save()
                return redirect('account_management')
            else:
                print(signup_form.errors)

    return render(request, 'account_management.html', {'login_form': login_form, 'signup_form': signup_form})