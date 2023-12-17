from django.shortcuts import render


def home(request):
    template_name = "index.html"
    return render(request, template_name)


def account_management(request):
    template_name = "account_management.html"
    return render(request, template_name)