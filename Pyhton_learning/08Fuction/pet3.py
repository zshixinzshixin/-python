def describe_pet(pet_name, animal_type = 'dog'):
    """"显示宠物的信息"""
    print(f"\nI haave o {animal_type}.")
    print(f"My {animal_type}'s name is {pet_name.title()}.")

describe_pet(pet_name='willie')
# 如果你发现在调用 describe_pet() 时，描述的大多是小狗，就可将形参 animal_type 的默认值设置为'dog'。
# 这样，当调用 describe_pet() 来描述小狗时，就可以不提供该信息
# 这里把pet_name放在第一位，或者采用关键字实参，否则会报错