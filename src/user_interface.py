def main_menu():
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

def add_comic_menu():
    welcome = "You have entered: Comic Book Addition!"
    menu = """Are you adding a single comic book or a collected edition?
    1) Single Comic Book
    2) Collected Edition
    3) Back
    
    Your selection: """

    print(welcome)

    user_input = input(menu)

    return user_input

def show_all_comics_menu():
    menu = """Would you like to see your single issue list, or your trade list?
    1) Single Comics List
    2) Trades List
    3) Back
    
    Your selection: """

    user_input = input(menu)

    return user_input 