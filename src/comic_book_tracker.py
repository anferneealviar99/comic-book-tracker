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
    
def menu():
    menuOptionString = "Select\n1. Add new comic\n2. Show current reading list\n3. Exit\n"

    menuOption = input(menuOptionString)

    print(menuOption)

    return menuOption

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
        
        count += 1

    if issue_found == True:
        details = api.issue(issues[count].id)
    else:
        details = None 

    return details

def main():
    api = login()

    menuOption = 0

    while True:
        menuOption = menu()

        match menuOption:
            case "1":
                title = input("Enter title of the comic book: ")
                publisher = input("Enter publisher name: ")
                comic_book = getComic(api, title, publisher)
                if comic_book is not None:
                    add_to_tracker(comic_book)
                else:
                    print("Please enter the following details:\n")
            case "2":
                print("Current List:")
            case "3":
                print("Exiting.")
                break

    

main()