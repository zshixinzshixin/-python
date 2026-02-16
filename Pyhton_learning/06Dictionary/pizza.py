pizza = {
    'crust': 'thick',
    'toppings': ['nushrooms', 'extra chees']
}

print(f"You orderd a {pizza['crust']}-crust pizza" " with the following toppings:")

for topping in pizza['toppings']:
    print(f"\t{topping}")
