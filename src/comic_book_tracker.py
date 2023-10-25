import mokkari, os, database
from dotenv import load_dotenv
from simyan.comicvine import Comicvine
from simyan.sqlite_cache import SQLiteCache
from user_interface import main_menu, add_comic_menu
from classes import ComicBookIssue

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
        "series_name": series_name,
        "issue_number": series_num,
        "year_began": year
    })

    # print(series_name, series_num)
    
    # series_matches = []

    for issue in issues:
        if title in issue.issue_name:
            issue_details = mokkari_api.issue(issue.id)
            return issue_details

    # if len(series_matches) > 1:
    #     year = input("Enter the beginning year of your comic book: ")
    
    #     for issue_details in series_matches:
    #         if issue_details.series.year_began == year:
    #             return issue_details
    # else:
    #     return series_matches[0]

def search_credits(credits, role):
    for credit in credits:
        roles = credit.role

        for role_entry in roles:
            if role.capitalize() == role_entry.name:
                return credit.creator
    


def add_comic_issue():
    title = input("Enter the name of the comic book issue: ")
    
    issue_details = search_issue(title)

    publisher = issue_details.publisher.name

    credits = issue_details.credits
    writer = search_credits(credits, "writer")
    penciller = search_credits(credits, "penciller")
    inker = search_credits(credits, "inker")
    colorist = search_credits(credits, "colorist")
    letterer = search_credits(credits, "letterer")
    editor = search_credits(credits, "editor")

    issue_entry = ComicBookIssue(title, publisher, writer, penciller, inker, colorist, letterer, editor)

    database.add_comic(issue_entry)


def add_new_comic():
    menuOption = 0

    menuOption = add_comic_menu()

    if int(menuOption) == 1:
        print("Adding a comic book issue...")
        add_comic_issue()
    elif int(menuOption) == 2:
        print("Adding collected editions...")
    elif int(menuOption) == 3:
        print("Going back...")


def main():
    database.create_tables()

    menuOption = 0

    while menuOption != '5':
        menuOption = main_menu()

        if int(menuOption) == 1:
            add_new_comic() 
        elif int(menuOption) == 2:
            print("UPCOMING COMICS")
        elif int(menuOption) == 3:
            print("YOUR CURRENT COMICS")
        elif int(menuOption) == 4:
            print("YOUR COMPLETED COMICS")
        elif int(menuOption) == 5:
            print("Exiting...")
            break
        else:
            print("Please enter a valid option.")

    

main()

#TODO separate menus into a file UserInterface.py
#TODO enter inputs which coincide with the Mokkari API - maybe? ComicVine API might be better honestly
