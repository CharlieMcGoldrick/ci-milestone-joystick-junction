from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import MainThread
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from .api.api import make_igdb_api_request
import json 

def home(request):
    template_name = "index.html"
    return render(request, template_name)

def make_main_thread_search_request(query):
    endpoint = 'games'
    query_body = f'fields *; where (category = 0 | category = 10) & version_title = null; search "{query}"; limit 10;'
    return make_igdb_api_request(endpoint, query_body)

def create_game_main_thread(request, game_id):
    game_name = request.POST.get('game_name')
    game = MainThread.objects.create(name=game_name, game_id=game_id)
    return HttpResponseRedirect(reverse('account_management'))

def search_created_main_threads(request):
    search_query = request.GET.get('search', '')
    threads = MainThread.objects.filter(name__icontains=search_query)
    thread_list = list(threads.values('name'))  # Convert QuerySet to list of dicts
    return JsonResponse(thread_list, safe=False)

# Account Management functions
def account_management(request):
    results = None
    form_submitted = False
    search_query = request.GET.get('search', '')  # Get the search query
    threads = MainThread.objects.filter(name__icontains=search_query)  # Filter threads based on the search query
    if request.method == 'POST':
        query = request.POST.get('query')
        results = make_main_thread_search_request(query)
        form_submitted = True
    return render(request, 'account_management.html', {'results': results, 'form_submitted': form_submitted, 'threads': threads})


def signup_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        signup_form = SignupForm(data)

        if signup_form.is_valid():
            user = signup_form.save()
            group, created = Group.objects.get_or_create(name='BasicUser')
            group.user_set.add(user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': signup_form.errors}, status=400)

    else:
        signup_form = SignupForm()

    return render(request, 'signup.html', {'signup_form': signup_form})


def check_username_email(request):
    data = json.loads(request.body)
    username = data.get('username')
    email = data.get('email')

    data = {
        'username_taken': User.objects.filter(username=username).exists(),
        'email_taken': User.objects.filter(email=email).exists()
    }

    return JsonResponse(data)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def promote_to_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username, groups__name='BasicUser').first()
        if user:
            user.is_staff = True
            user.save()
            return redirect('account_management')
        else:
            # Handle case where user does not exist or is not in BasicUser group
            pass
    return redirect('account_management')


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