from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ComicBook, UserComic, Role, Person, ComicRole
import requests 
import regex as re

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
        
        params = {}
        
        if series:
            params['series'] = series
        
        if year:
            params['year'] = year
        
        if issue:
            params['issue'] = issue
            
        try:
            response = requests.get(url, 
                                    auth=(settings.METRON_API_USERNAME, settings.METRON_API_PASSWORD),
                                    params=params
            )
            response.raise_for_status()
            data = response.json()
            
            results_list = data["results"]
            
            if len(results_list) > 1: 
                return render(request, 'select_comic.html', {'comics': results_list})

            else:
                issue_details = results_list[0]
                
                comic_id = issue_details['id']
                
                comic = ComicBook.objects.get_or_create(
                    comic_id=comic_id,
                    defaults={
                        'title': issue_details['issue'],
                        'series': issue_details['series'],
                        'year': issue_details['year'],
                        'cover_image_url': issue_details['image'] 
                    }
                )
                
                return redirect('fetch_comic_details', comic_id=comic_id)
            
        except requests.exceptions.RequestException as e:
            return render(request, 'error.html', {'message': str(e)})
        
@login_required
def fetch_comic_details(request, comic_id):
    try:
        comic = ComicBook.objects.get(id=comic_id)
        details_url = f"{settings.METRON_API_URL}/issue/{comic.comic_id}"
        
        response = requests.get(
            details_url,
            auth=(settings.METRON_API_USERNAME, settings.METRON_API_PASSWORD)
        )
        
        response.raise_for_status()
        issue_details = response.json()
        
        comic.publisher = issue_details['publisher']['name']
        
        process_comic_roles(issue_details, comic)

        UserComic.objects.get_or_create(user=request.user, comic=comic)

        return redirect('user_comics')

    except ComicBook.DoesNotExist:
        return render(request, 'error.html', {'message': 'Comic was not found.'})
    
    except requests.exceptions.RequestException as e:
        return render(request, 'error.html', {'message': str(e)})
    
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