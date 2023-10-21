import mokkari, getpass

class TrackerEntry:
    def __init__(self, comicBookDetails, status, rating=None, review=None):
        self.comicBookDetails = comicBookDetails
        self.status = status 
        self.rating = rating 
        self.review = review  

class ComicBook:
    def __init__(self, name, writer, penciller, inker, colorist, letterer, editor):
        self.name = name 
        self.writer = writer
        self.penciller = penciller 
        self.inker = inker
        self.colorist = colorist
        self.letterer = letterer
        self.editor = editor 

    def printDetails(self):
        print(f'Comic Book Title: {self.name}')
        print(f'Writer: {self.writer}')
        print(f'Penciller: {self.penciller}')
        print(f'Inker: {self.inker}')
        print(f'Colorist: {self.colorist}')
        print(f'Letterer: {self.letterer}')
        print(f'Editor: {self.editor}')

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

def search(api, title, publisher):
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
                comic_book = search(api, title, publisher)
                add_to_tracker(comic_book)
            case "2":
                print("Current List:")
            case "3":
                print("Exiting.")
                break

    

main()