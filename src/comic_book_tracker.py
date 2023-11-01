import mokkari, os, database
from dotenv import load_dotenv
from user_interface import main_menu, add_comic_menu, show_all_comics_menu
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

    print(issue_obj)

    if len(issue_obj) > 0:
        return mokkari_api.issue(issue_obj[0].id) 
    else:
        return None

    # for issue in issues:
    #     if title in issue.issue_name:
    #         issue_details = mokkari_api.issue(issue.id)
    #         return issue_details

def search_credits(credits, role):
    creators = []
    for credit in credits:
        roles = credit.role

        for role_entry in roles:
            if role.capitalize() == role_entry.name:
                creators.append(credit.creator)

    return ", ".join(str(creator) for creator in creators)
    
def get_issue_components (issue_string):
    issue_components = issue_string.split("#")
    series_num = issue_components[1].strip()

    if "(" in issue_components[0]:
        series_name_year = issue_components[0].split("(")
        series_name = series_name_year[0].strip()
        year = series_name_year[1].strip(")")
        return [series_name, year, series_num]
    else:
        series_name = issue_components[0]
        return [series_name, series_num]

def find_issues_in_range(issue):
    issue_comp = issue.split("#")
    issue_range = issue_comp[1].split('-')
    series_name = issue_comp[0].strip()

    all_issues = []
    print(issue_range)
    for i in range(int(issue_range[0]), int(issue_range[1]) + 1, 1):
        issue_string = f'{series_name} #{i}'
        all_issues.append(issue_string)
    
    return all_issues 

def search_issue_range(issues_set, issue_details_list):
    search_criteria = get_issue_components(issues_set[0])

    issues_list = mokkari_api.issues_list(
        {
            'series_name': search_criteria[0],
            'issue_number': search_criteria[2],
            'year_began': search_criteria[1]
        }
    )

    issues_set = set(issues_set)

    for issue in issues_list:
        if issue.issue_name in issues_set:
            found_issue = mokkari_api.issue(issue.id)
            issue_details_list.append(found_issue)

def search_issues(issues_list, issue_details_list, publisher):
    for issue in issues_list:

        issue_num = issue.split("#")[1]
        if '-' in issue_num:
            issues_set = find_issues_in_range(issue)
            search_issue_range(issues_set, issue_details_list)
        else:
            issue_details = search_issue(issue, publisher)
            issue_details_list.append(issue_details)

def add_graphic_novel():
    title = input("Enter the name of the graphic novel: ")
    
    issues_list = input("Please enter all issues associated with this graphic novel/trade paperback: ").split(",")

    issues_list = [issues.strip() for issues in issues_list]

    publisher = input("Please enter the name of the publisher: ")
    
    issue_details_list = []

    search_issues(issues_list, issue_details_list, publisher)

    writers = []
    pencillers = []
    inkers = []
    colorists = []
    letterers = []
    editors = []

    comic_issues = []

    for issue in issue_details_list:
        
        if issue is None:
            pass
        else:
            issue_series = issue.series.name
            issue_volume = issue.series.volume
            issue_number = issue.number
            print(issue.series.name, issue.series.volume, issue.number)
            publisher = issue.publisher.name

            credits = issue.credits

            writer = search_credits(credits, "writer")

            if writer is None:
                writer = search_credits(credits, "plot")
                writer = search_credits(credits, "story")
                print(writer)
            
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
            
            comic_issues.append(single_issue)

            if database.find_comic(single_issue) is None:
                database.add_comic(single_issue)
            else:
                print(f'{issue_series} Vol. {issue_volume} #{issue_number}  already exists in your list. Skipping this entry.')

    all_issues = ", ".join(issues_list)
    
    if not None in writers:
        all_writers = ", ".join(writers)
    else:
        all_writers = ""

    if not None in pencillers:
        all_pencillers = ", ".join(pencillers)
    else:
        all_pencillers = ""
    
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
    
    trade_id = database.add_trade(trade)

    database.add_trade_id(trade_id, comic_issues)

    print(f"{title} has been added to your list!")

def add_comic_issue(title, publisher):
    try:
        issue_details = search_issue(title, publisher)

        if issue_details is None:
            raise InvalidComicIssueException
        else:
            publisher = issue_details.publisher.name
            series_name = issue_details.series.name
            volume = issue_details.series.volume
            number = issue_details.number
            credits = issue_details.credits
            writer = search_credits(credits, "writer")
            penciller = search_credits(credits, "penciller")
            if penciller is None:
                penciller = search_credits(credits, "artist")
            
            inker = search_credits(credits, "inker")
            if inker is None:
                inker = search_credits(credits, "artist")

            colorist = search_credits(credits, "colorist")
            letterer = search_credits(credits, "letterer")
            editor = search_credits(credits, "editor")

            issue_entry = ComicBookIssue(series_name, volume, number, publisher, writer, penciller, inker, colorist, letterer, editor)

            if database.find_comic(issue_entry) is None:
                database.add_comic(issue_entry)
                print(f'{title} was added to your list!')
            else:
                print(f'{title} already exists in your list.')
            

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


def print_comics_list(comics):
    print("----------ALL COMICS----------")

    for comic in comics:
        series_name = comic[1]
        series_volume = comic[2]
        issue_number = comic[3]

        writer = comic[5]
        penciller = comic[6]

        print(f'{series_name} Vol. {series_volume} #{issue_number}, by {writer} and {penciller}')



def print_trades_list(trades):
    print("----------ALL TRADES----------")
    
    for trade in trades:
        trade_name = trade[1]
        trade_issues = trade[3]

        writers = trade[4]
        pencillers = trade[5]
            
        print(f'{trade_name} ({trade_issues}) by {writers} and {pencillers}')

def show_all_comics():
    menuOption = 0

    while menuOption != '3':
        menuOption = show_all_comics_menu()
        if menuOption == '1':
            comics = database.get_comics()
            print_comics_list(comics)
        elif menuOption == '2':
            trades = database.get_trades() 
            print_trades_list(trades)
        elif menuOption == '3':
            print("Going back...")
        else:
            print("Please enter a valid option.")

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
            show_all_comics()
        elif int(menuOption) == 4:
            print("YOUR COMPLETED COMICS")
        elif int(menuOption) == 5:
            print("Exiting...")
            break
        else:
            print("Please enter a valid option.")


main()