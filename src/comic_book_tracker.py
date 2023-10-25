import mokkari, os
from dotenv import load_dotenv
from simyan.comicvine import Comicvine
from simyan.sqlite_cache import SQLiteCache
from user_interface import main_menu, add_comic_menu

load_dotenv('key.env')
mokkari_user = os.getenv('MOKKARI_USERNAME')
mokkari_password = os.getenv('MOKKARI_PASSWORD')

mokkari_api = mokkari.api(mokkari_user, mokkari_password)

def add_comic_issue():
    series = input("Enter the name of the comic book issue: ")
    

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
