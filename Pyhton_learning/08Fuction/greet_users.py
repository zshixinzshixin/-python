def greet_users(names):
    """"向列表的每个用户发出简单的的问候"""
    for name in names:
        msg = f"Hello, {name.title()}"
        print(msg)

usernames = ['hannah', 'ty', 'margot']
greet_users(usernames)
