# 可以导入单个类/多个类/整个模块/整个模块所有类
# import Car
# from car impotr *
# 不推荐导入整个模块所有类，原因有二：
# 第一，最好只需要看一下文件开头的 import 语句，就能清楚地知道程序使用了哪些类。
# 但这种导入方式没有明确地指出使用了模块中的哪些类。
# 第二，这种导入方式还可能引发名称方面的迷惑。
# 如果不小心导入了一个与程序文件中的其他东西同名的类，将引发难以诊断的错误。
# 这里之所以介绍这种导入方式，是因为虽然不推荐，但你可能在别人编写的代码中见到它。
from car import Car,ElectricCar

my_new_car = Car('audi', 'a4', 2024)
print(my_new_car.get_descriptive_name())

my_new_car.read_odometer()

my_new_car.odometer_reading = 23
my_new_car.read_odometer()

my_new_car.update_adometer(24)
my_new_car.read_odometer()
my_new_car.update_adometer(23)

print("------")
my_userd_car = Car('subaru', 'outback', 2019)
print(my_userd_car.get_descriptive_name())

my_userd_car.update_adometer(23_500)
my_userd_car.read_odometer

my_userd_car.increment_odometer(100)
my_userd_car.read_odometer()

print("------")
my_mustang = Car('ford', 'mustang', 2024)
print(my_userd_car.get_descriptive_name())
my_leaf = ElectricCar('nissan', 'leaf', 2024)
print(my_leaf.get_descriptive_name())