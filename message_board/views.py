from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import MainThread
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from datetime import datetime
from .api.api import make_igdb_api_request
import json 

def home(request):
    template_name = "index.html"
    return render(request, template_name)

def make_main_thread_search_request(query):
    endpoint = 'games'
    query_body = f'fields name,genres.name,platforms.name,summary,involved_companies.company.name,game_engines.name,aggregated_rating; where (category = 0 | category = 10) & version_title = null; search "{query}"; limit 10;'
    return make_igdb_api_request(endpoint, query_body)

def search_games_for_main_thread(request):
    search_query = request.GET.get('query', '')
    results = make_main_thread_search_request(search_query)
    return JsonResponse(results, safe=False)

def create_game_main_thread(request, game_id):
    print(request.body)
    data = json.loads(request.body)
    print(data)  # Log the request data
    game_name = data.get('game_name')
    genres = json.loads(data.get('genres', '[]'))
    platforms = json.loads(data.get('platforms', '[]'))
    summary = data.get('summary')
    involved_companies = json.loads(data.get('involved_companies', '[]'))
    game_engines = json.loads(data.get('game_engines', '[]'))
    aggregated_rating = data.get('aggregated_rating')

    # Check if a MainThread with the given game_id already exists
    if MainThread.objects.filter(game_id=game_id).exists():
        return JsonResponse({'error': 'A thread for this game already exists.'}, status=400)

    # Create a new MainThread instance
    try:
        game = MainThread(
            name=game_name,
            game_id=game_id,
            summary=summary,
            aggregated_rating=aggregated_rating
        )
        game.set_genres(genres)
        game.set_platforms(platforms)
        game.set_involved_companies(involved_companies)
        game.set_game_engines(game_engines)
        game.save()
        return JsonResponse({'success': 'Thread created successfully.'})
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

def search_created_main_threads(request):
    search = request.GET.get('search', '')
    threads = MainThread.objects.filter(name__icontains=search).values()
    thread_list = list(threads)
    return JsonResponse(thread_list, safe=False)

@require_POST
def delete_a_main_thread(request):
    try:
        thread_id = request.POST.get('thread_id')
        print('Thread ID:', thread_id)  # Log the thread ID

        thread = MainThread.objects.get(id=thread_id)
        thread.delete()

        return JsonResponse({'status': 'success'})
    except MainThread.DoesNotExist:
        print('MainThread not found')  # Log the error
        return JsonResponse({'error': 'MainThread not found'}, status=404)
    except Exception as e:
        print('Error:', e)  # Log any other exceptions
        return JsonResponse({'error': 'An error occurred'}, status=500)

# Account Management functions
def account_management(request):
    results = None
    form_submitted = False
    return render(request, 'account_management.html')


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