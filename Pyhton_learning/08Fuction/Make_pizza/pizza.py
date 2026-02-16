def make_pizza(size, *toppings):
    """"打印顾客点的所以配料"""
    print(f"\nMake a {size}-inch pizza with the followint toppings:")
    for topping in toppings:
        print(f"-{topping}")
        
# 使用任意数量的实参
# 使用位置实参+任意数量的实参