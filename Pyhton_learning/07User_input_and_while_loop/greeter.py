name = input("Please enter your name:")
print(f"\nHello,{name}!")

# prompt提示
prompt = "If you share your name, we can personalize the message you see."
prompt += "\nWhat is your first name:"
name = input(prompt)
print(f"\n Hello,{name}!")
# 当prompt超过一行的时候，先定义prompt变量，通过+=变量添加第二行