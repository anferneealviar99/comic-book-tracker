from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ComicBook, UserComic, Role, Person, ComicRole
import requests 
import regex as re


def homepage_view(request):
    # Change the view based on whether the visitor is authenticated or not 
    if request.user.is_authenticated:
        followed_comics = UserComic.objects.filter(user=request.user).select_related('comic')
        return render(request, 'home.html', {'followed_comics': followed_comics})
    else:
        return render(request, 'home.html')

@login_required
def user_comics(request):
    # Fetch comics followed by the user
    followed_comics = UserComic.objects.filter(user=request.user).select_related('comic')
    
    return render(request, 'user_comics.html', {'followed_comics': followed_comics})

@login_required
def add_comic(request):
    if request.method == 'POST':
        comic_search_input = request.POST.get('comic_title')
        series, year, issue = parse_comic_search_input(comic_search_input)
        
        # Create flexible cache key based on available search parameters
        search_cache_key = f"search_results_{"_".join(series.split(" ")) or ""}_{year or ""}_{issue or ""}"
        cached_results = cache.get(search_cache_key)
        
        if cached_results:
            results_list = cached_results
        else:
            url = f'{settings.METRON_API_URL}/issue/'
            params = {}
            
            if series:
                params['series_name'] = series
            
            if year:
                params['series_year_began'] = year
            
            if issue:
                params['number'] = issue
                
            try:
                response = requests.get(url, 
                                        auth=(settings.METRON_API_USERNAME, settings.METRON_API_PASSWORD),
                                        params=params
                )
                response.raise_for_status()
                data = response.json()
                
                results_list = data["results"]
                
                cache.set(search_cache_key, results_list, timeout=60*60*24)
            
            except requests.exceptions.RequestException as e:
                return render(request, 'error.html', {'message': str(e)})
            
        if len(results_list) > 1: 
            return render(request, 'select_comic.html', {'comics': results_list})

        else:
            issue_details = results_list[0]
        
            comic_id = issue_details['id']
            
            comic_cache_key = f'comic_data_{comic_id}'
            
            # Check if the data is cached
            cached_comic_data = cache.get(comic_cache_key)
            
            if cached_comic_data:
                comic_data=cached_comic_data
            else:
                comic_data = {
                    'comic_id': comic_id,
                    'title': issue_details['issue'],
                    'series': issue_details['series'],
                    'series_year': issue_details['series']['year_began'],
                    'cover_image_url': issue_details['image']
                }
                
                cache.set(comic_cache_key, comic_data, timeout=60*60*24)
            
            
            comic = ComicBook(
                        comic_id=comic_id,
                        title = issue_details['issue'],
                        series = issue_details['series'],
                        series_year = issue_details['series']['year_began'],
                        cover_image_url = issue_details['image'] 
                    )
            
            comic.save()
            
            return redirect('fetch_comic_details', comic_id=comic_id)
    
    return render(request, 'add_comic.html')

@login_required
def select_comic(request):
    if request.method == 'POST':
        comic_id = request.POST.get('selected-comic-name')
        cache_comic_key = f'comic_issue_data_{comic_id}'
        cached_details = cache.get(cache_comic_key)
        
        if cached_details:
            issue_details = cached_details
        else:
            url = f'{settings.METRON_API_URL}/issue/{comic_id}/'
            
            response = requests.get(url,
                                    auth=(settings.METRON_API_USERNAME, settings.METRON_API_PASSWORD))
            
            response.raise_for_status()
            issue_details = response.json()
            
            cache.set(cache_comic_key, issue_details, 60*60*24)
        
        comic_id = comic_id
        series_details = issue_details['series']
        series_name = series_details['name']
        series_id = series_details['id']
        
        cached_series_key = f'comic_series_{series_id}'
        cached_series = cache.get(cached_series_key)
        
        # Check if the series exists in cache
        if cached_series:
            series_details = cached_series
        else: 
            series_url=f'{settings.METRON_API_URL}/series/{series_id}/'
            series_response = requests.get(series_url,
                                        auth=(settings.METRON_API_USERNAME, settings.METRON_API_PASSWORD))
            
            series_response.raise_for_status()
            series_details = series_response.json()

            cache.set(cached_series_key, series_details, 60*60*24)
        
        series_year = series_details['year_began']
        
        number=issue_details['number']
        
        title = f'{series_name} ({series_year}) #{number}'
        
        publisher = issue_details['publisher']['name']
        image = issue_details['image']
    
        comic = ComicBook(
            comic_id=comic_id,
            title=title,
            series=series_name,
            number=number,
            series_year=series_year,
            cover_image_url=image,
            publisher=publisher
        )
        
        comic.save()
        
        return redirect('fetch_comic_details', comic_id)

    return redirect('add_comic')
           
@login_required
def fetch_comic_details(request, comic_id=None):
    comic = ComicBook.objects.get(comic_id=comic_id)
    
    comic_cache_key = f'comic_issue_data_{comic_id}'
    comic_details = cache.get(comic_cache_key)
    
    if comic_details:
        issue_details = comic_details
    else:
        try:
            comic = ComicBook.objects.get(comic_id=comic_id)
            details_url = f"{settings.METRON_API_URL}/issue/{comic.comic_id}/"
            
            response = requests.get(
                details_url,
                auth=(settings.METRON_API_USERNAME, settings.METRON_API_PASSWORD)
            )
        
            response.raise_for_status()
            issue_details = response.json()
        except requests.exceptions.RequestException as e:
            return render(request, 'error.html', {'message': str(e)})
    
    comic.publisher = issue_details['publisher']['name']
    
    process_comic_roles(issue_details, comic)

    user_comic, _ = UserComic.objects.get_or_create(user=request.user, comic=comic)
    
    user_comic.save()

    return redirect('user_comics')   
    
def parse_comic_search_input(comic_search_input):
    """
    Parse user input to extract series name, year and issue
    Assumes input format is something e.g. "Batman (2016) #1" or Superman #1
    Returns: (series, year, issue)
    """
    match = re.match(r"^(.*?)(?:\s\((\d{4})\))?\s?#(\d+)?$", comic_search_input.strip())

    if match:
        series = match.group(1).strip()
        year = match.group(2) if match.group(2) else None 
        issue = match.group(3).strip() if match.group(3) else None
    else:
        series, year, issue = comic_search_input.strip(), None, None 
        
    return series, year, issue

def process_comic_roles(data, comic):
    """Processes and saves roles associated with a comic using data from the Metron API

    Args:
        data (JSON): the data containing issue details, obtained by GET request
        comic (ComicBook): the comic book in question
    """
    
    role_data = data['credits']
    
    for creator in role_data:
        creator_name = creator['creator']
        roles = creator['role']
        person, _ = Person.objects.get_or_create(name=creator_name)
        
        if len(roles) > 1:
            for role in roles:
                role_name = role['name']
                role, _ = Role.objects.get_or_create(name=role_name)
                ComicRole.objects.get_or_create(comic=comic, person=person, role=role)
        else:
            role = roles[0]
            role_name = role['name']
            role, _ = Role.objects.get_or_create(name=role_name)
            

        
        ComicRole.objects.get_or_create(comic=comic, person=person, role=role)