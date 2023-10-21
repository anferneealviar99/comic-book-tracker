import mokkari, getpass



def login():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    try:
        api = mokkari.api(username, password)
    except mokkari.exceptions.AuthenticationError as e:
        print("Invalid user name and password.")

    print("Login successful.")

    return api
    
def gen_main_menu():
    welcome = "Welcome to the Comic Book Tracker!"
    menu  = """Please select one of the following options:
    1) Add new comic
    2) View upcoming comics
    3) View all comics in tracker
    4) View read comics
    5) Exit
    
    Your selection: """

    print(welcome)
    
    user_input = input(menu)
    
    return user_input

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

    

def main():
    api = login()

    menuOption = 0

    while True:
        menuOption = gen_main_menu()

        match int(menuOption):
            case 1:
                title = input("Enter title of the comic book: ")
                publisher = input("Enter publisher name: ")
                comic_book = getComic(api, title, publisher)
                if comic_book is not None:
                    addToTracker(comic_book)
                else:
                    print("Please enter the following details:\n")
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
#TODO enter inputs which coincide with the Mokkari API 
