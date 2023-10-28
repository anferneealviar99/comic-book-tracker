import mokkari, os, database
from dotenv import load_dotenv
from user_interface import main_menu, add_comic_menu
from classes import ComicBookIssue, Trade, InvalidComicIssueException

load_dotenv('key.env')
mokkari_user = os.getenv('MOKKARI_USERNAME')
mokkari_password = os.getenv('MOKKARI_PASSWORD')

mokkari_api = mokkari.api(mokkari_user, mokkari_password)

#TODO any individual issues inside a trade should be added onto the single comics as well
def search_issue(title, publisher):

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
        "year_began": year,
        "publisher_name": publisher
    })

    issue_obj = [issue for issue in issues if issue.issue_name == title]
    
    return mokkari_api.issue(issue_obj[0].id)

    # for issue in issues:
    #     if title in issue.issue_name:
    #         issue_details = mokkari_api.issue(issue.id)
    #         return issue_details

def search_credits(credits, role):
    for credit in credits:
        roles = credit.role

        for role_entry in roles:
            if role.capitalize() == role_entry.name:
                return credit.creator
    
def find_issues_in_range(issue):
    issue_comp = issue.split("#")
    issue_range = issue_comp[1].split('-')
    series_name = issue_comp[0].strip()

    all_issues = []
    for i in range(int(issue_range[0]), int(issue_range[1]) + 1, 1):
        issue_string = f'{series_name} #{i}'
        all_issues.append(issue_string)
    
    return all_issues 

def search_issues(issues_list, issue_details_list, publisher):
    for issue in issues_list:
        if '-' in issue:
            issues_string = find_issues_in_range(issue)
            issue_details = search_issues(issues_string, issue_details_list, publisher)
        else:
            issue_details = search_issue(issue, publisher)
            issue_details_list.append(issue_details)

def add_graphic_novel():
    title = input("Enter the name of the graphic novel: ")
    
    issues_list = input("Please enter all issues associated with this graphic novel/trade paperback: ").split(",")

    publisher = input("Please enter the name of the publisher: ")
    
    issue_details_list = []

    search_issues(issues_list, issue_details_list, publisher)

    writers = []
    pencillers = []
    inkers = []
    colorists = []
    letterers = []
    editors = []


    for issue in issue_details_list:
        issue_series = issue.series.name
        issue_volume = issue.series.volume
        issue_number = issue.number
        publisher = issue.publisher.name

        credits = issue.credits

        writer = search_credits(credits, "writer")
        
        if writer not in writers:
            writers.append(writer)

        penciller = search_credits(credits, "penciller")

        if penciller is None:
            penciller = search_credits(credits, "artist")

        if penciller not in pencillers:
            pencillers.append(penciller)

        inker = search_credits(credits, "inker")

        if inker is None:
            inker = search_credits(credits, "artist")

        if inker not in inkers:
            inkers.append(inker)

        colorist = search_credits(credits, "colorist")

        if colorist not in colorists:
            colorists.append(colorist)

        letterer = search_credits(credits, "letterer")

        if letterer not in letterers:
            letterers.append(letterer)

        editor = search_credits(credits, "editor")

        if editor not in editors:
            editors.append(editor)

        single_issue = ComicBookIssue(issue_series, 
                                      issue_volume,
                                      issue_number, 
                                      publisher,
                                      writer,
                                      penciller,
                                      inker,
                                      colorist,
                                      letterer, 
                                      editor)
        
        database.add_comic(single_issue)

    all_issues = ", ".join(issues_list)
    all_writers = ", ".join(writers)

    if not None in pencillers:
        all_pencillers = ", ".join(pencillers)
    
    if None in inkers:
        all_inkers = ""
    else:
        all_inkers = ", ".join(inkers)

    if None in colorists:
        all_colorists=""
    else:
        all_colorists = ", ".join(colorists)

    if None in letterers:
        all_letterers = ""
    else:
        all_letterers = ", ".join(letterers)

    if None in editors:
        all_editors=""
    else:
        all_editors = ", ".join(editors)

    trade = Trade(title, publisher, all_issues, all_writers, all_pencillers,
                  all_inkers, all_colorists, all_letterers, all_editors)
    
    database.add_trade(trade)

    print(f"{title} has been added to your list!")

def add_comic_issue(title, publisher):
    try:
        issue_details = search_issue(title, publisher)

        if issue_details is None:
            raise InvalidComicIssueException
        else:
            publisher = issue_details.publisher.name
            series_name = issue_details.series.name
            number = issue_details.number
            credits = issue_details.credits
            writer = search_credits(credits, "writer")
            penciller = search_credits(credits, "penciller")
            inker = search_credits(credits, "inker")
            colorist = search_credits(credits, "colorist")
            letterer = search_credits(credits, "letterer")
            editor = search_credits(credits, "editor")

            issue_entry = ComicBookIssue(series_name, number, publisher, writer, penciller, inker, colorist, letterer, editor)

            database.add_comic(issue_entry)

    except InvalidComicIssueException:
        print("Comic issue was not found")

def add_new_comic():
    menuOption = 0

    while (int(menuOption) != 3):
        menuOption = add_comic_menu()
        if int(menuOption) == 1:
            print("Adding a comic book issue...")
            title = input("Enter the name of the comic book issue: ")
            publisher = input("Enter the name of the publisher: ")
            add_comic_issue(title, publisher)
        elif int(menuOption) == 2:
            print("Adding collected editions...")
            add_graphic_novel()
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