import mokkari, os
from dotenv import load_dotenv
from simyan.comicvine import Comicvine
from simyan.sqlite_cache import SQLiteCache
from user_interface import main_menu, add_comic_menu

load_dotenv('key.env')
comicvine_api_key = os.getenv('COMICVINE_API_KEY')
mokkari_user = os.getenv('MOKKARI_USERNAME')
mokkari_password = os.getenv('MOKKARI_PASSWORD')

mokkari_api = mokkari.api(mokkari_user, mokkari_password)
comicvine_api = Comicvine(api_key=comicvine_api_key, cache=SQLiteCache())

def getComic(api, title, publisher):
    info = title.split("#")

    print(info)

    name = info[0]
    number = info[1]

    issues = api.issues_list({
        "series": name,
        "number": number,
        "publisher_name": publisher,
    })
    

    issue_found = False
    count = 0
    while issue_found is False and count < len(issues):
        if issues[count].issue_name == title:
            issue_found = True 
            break
        
        count += 1

    if issue_found == True:
        details = api.issue(issues[count].id)
    else:
        details = None 

    return details

def getSeriesDetails(comicSeries):
    return[comicSeries.name, comicSeries.volume]


def getWriter(creators):
    for creator in creators:
        creator_role = creator.role
        for role in creator_role:
            if role.name.capitalize() == "Writer":
                return creator.creator

def addToTracker(comic_book):
    series = getSeriesDetails(comic_book.series)

    print(series)

    publisher = comic_book.publisher
    number = comic_book.number
    story_titles = comic_book.story_titles
    cover_date = comic_book.cover_date
    creators = comic_book.credits

    writer = getWriter(creators) 
    print(writer)

def add_new_comic():
    menuOption = 0

    menuOption = add_comic_menu()

    match int(menuOption):
        case 1:
            print("Adding a comic book issue...")
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
