import os

username = input("Username: ")

folder = "username_checks"

if type(username) == str:
    os.system(f"sherlock {username} -fo {folder}")
    
elif type(username) == list:
    for name in username:
        print(f"Checking username: {name}")
        os.system(f"sherlock {name} -fo {folder}")
