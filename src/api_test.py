import mokkari, os
from dotenv import load_dotenv

load_dotenv('key.env')
username = os.getenv('MOKKARI_USERNAME')
password = os.getenv('MOKKARI_PASSWORD')

try:
    api = mokkari.api(username, password)
except mokkari.exceptions.AuthenticationError as e:
    print("Invalid user name and password.")

# Get all Marvel comics for the week of 2021-06-07
asm = api.issues_list({"series_name": "Amazing Spider-Man", "issue_number": "50", "year_began": "1963", "publisher_name": "marvel"})

# Print the results
for i in asm:
    print(f"{i.id} {i.issue_name}")


