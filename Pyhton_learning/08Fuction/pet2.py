def describe_pet(animal_type, pet_name):
    """"显示宠物的信息"""
    print(f"\nI haave o {animal_type}.")
    print(f"My {animal_type}'s name is {pet_name.title()}.")

describe_pet(animal_type='hamster', pet_name='harry')
# 关键字实参的顺序无关紧要