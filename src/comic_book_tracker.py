import mokkari, os
from dotenv import load_dotenv
from simyan.comicvine import Comicvine
from simyan.sqlite_cache import SQLiteCache
from user_interface import main_menu, add_comic_menu
import regex as re 

load_dotenv('key.env')
mokkari_user = os.getenv('MOKKARI_USERNAME')
mokkari_password = os.getenv('MOKKARI_PASSWORD')

mokkari_api = mokkari.api(mokkari_user, mokkari_password)

def search_issue(title):

    title_components = title.split("#")
    series_num = title_components[1].strip()

    if "(" in title_components[0]:
        series_name_year = title_components[0].split("(")
        series_name = series_name_year[0].strip()
        year = series_name_year[1].strip(")")
    else:
        series_name = title_components[0]

    issues = mokkari_api.issues_list({
        "series": {
            'name': series_name,
            'year_began': year
        },
        "number": series_num
    })

    print(series_name, series_num)
    
    series_matches = []

    for issue in issues:
        if series_name in issue.series.name:
            issue_details = mokkari_api.issue(issue.id)
            series_matches.append(issue_details)

    if len(series_matches) > 1:
        year = input("Enter the beginning year of your comic book: ")
    
        for issue_details in series_matches:
            if issue_details.series.year_began == year:
                return issue_details
    else:
        return series_matches[0]
            
            

def add_comic_issue():
    title = input("Enter the name of the comic book issue: ")
    
    issue_details = search_issue(title)

    print(issue_details)


    

def add_new_comic():
    menuOption = 0

    menuOption = add_comic_menu()

    match int(menuOption):
        case 1:
            print("Adding a comic book issue...")
            add_comic_issue()
        case 2:
            print("Adding collected editions...")
        case 3:
            print("Going back...")


def main():
    menuOption = 0

    while menuOption != '5':
        menuOption = main_menu()

        match int(menuOption):
            case 1:
                add_new_comic() 
            case 2:
                print("UPCOMING COMICS")
            case 3:
                print("YOUR CURRENT COMICS")
            case 4:
                print("YOUR COMPLETED COMICS")
            case 5:
                print("Exiting...")
                break
            case _:
                print("Please enter a valid option.")

    

main()

#TODO separate menus into a file UserInterface.py
#TODO enter inputs which coincide with the Mokkari API - maybe? ComicVine API might be better honestly
