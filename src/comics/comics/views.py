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
                url = f'{settings.METRON_API_URL}/issue/{comic_id}'
                
                # return handle_comic_data(request, url)
            
        except requests.exceptions.RequestException as e:
            return render(request, 'error.html', {'message': str(e)})
        
# def handle_comic_data(request, url):
#     try:
#         response = requests.get(url,
#                                 auth=(settings.METRON_API_USERNAME, settings.METRON_API_PASSWORD))
#         response.raise_for_status()
#         issue_data = response.json()
        
#         if isinstance(issue_data, dict):
#             comic, created = ComicBook.objects.get_or_create(
#                 comic_id = comic_id,
#                 defaults={
#                     'title': issue_data['issue']
#                 }
#             )
#     except requests.exceptions.RequestException as e:
#         return render(request, 'error.html', {'message': str(e)})
        