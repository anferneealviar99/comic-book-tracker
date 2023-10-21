import mokkari 
import getpass

username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")

try:
    api = mokkari.api(username, password)
except mokkari.exceptions.AuthenticationError as e:
    print("Invalid user name and password.")

# Test publisher

pub_result = api.publisher(2)

pub_name = pub_result.name
pub_founded = pub_result.founded
pub_desc = pub_result.desc

print(f'Name: {pub_name}\nFounded: {pub_founded}\nDescription: {pub_desc}')



