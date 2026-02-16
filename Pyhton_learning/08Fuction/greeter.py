def greet_user():
    """"这是简单的问候语"""
    print("Hello!")

greet_user()

# 这里向函数传递参数
def greet_user2(username):
    """"这是简单的问候语"""
    print(f"Hello, {username.title()}!")

greet_user2('jesse')