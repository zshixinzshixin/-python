requested_toppings = ['mushrooms', 'extra cheese']

if 'mushrooms' in requested_toppings:
    print("Adding mushrooms.")
if 'peepperoni' in requested_toppings:
    print("Adding pepperoni")
if 'extra cheese' in requested_toppings:
    print("Adding extra cheese.")

print("\nFinshed making your pizza!")

# 检查了每个条件，所以将在比萨中添加蘑菇并多加芝士

requested_toppings = ['mushrooms', 'green peppers', 'extra cheese']

for requested_topping in requested_toppings:
    print(f"Adding {requested_topping}")

print("\nFinshed making your pizza")

# 输出很简单，但是如果green pepper用完了呢？

requested_toppings = ['mushrooms', 'green peppers', 'extra cheese']

for requested_topping in requested_toppings:
    if requested_topping == 'green peppers':
        print("Sorry,we are out of green peppers right now.")
    else:
        print(f"Adding {requested_topping}.")

print("\nFinshed making your pizza")

# 增加了一个判断条件

requested_toppings = []
if requested_toppings:
    for requested_topping in requested_toppings:
        print(f"Adding {requested_topping}.")
    print("\nFinshed making your pizza!")
else:
    print("Are you sure you want a plain pizza?")

# 增加对空表格的检查