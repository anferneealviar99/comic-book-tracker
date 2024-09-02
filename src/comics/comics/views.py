from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ComicBook, UserComic, Role, Person, ComicRole
import requests 

@login_required
def user_comics(request):
    # Fetch comics followed by the user
    followed_comics = UserComic.objects.filter(user=request.user).select_related('comic')
    
    return render(request, 'user_comics.html', {'followed_comics': followed_comics})

@login_required
def add_comic(request):
    if request.method == 'POST':
        comic_search_input = request.POST.get('comic_search_input')
        
        series, year, issue = parse_comic_search_input(comic_search_input)
        
        url = f'{settings.METRON_API_URL}/issue/'
        
        try:
            response = requests.get(url, 
                                    auth=(settings.METRON_API_USERNAME, settings.METRON_API_PASSWORD)
            )
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list) and len (data) > 1:
                return render(request, 'select_comic.html', {'comics': data})

            if isinstance(data, dict):
                comic, created = ComicBook.objects.get_or_create(
                    comic_id =data['comic_id'],
                    defaults={
                        'title': data['title']
                    }
                )
            
        except requests.exceptions.RequestException as e:
            return render(request, 'error.html', {'message': str(e)})
        