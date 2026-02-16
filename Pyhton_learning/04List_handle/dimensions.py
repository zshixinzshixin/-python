# 代码功能：演示元组的使用
# 尺寸
dimensions = (200, 50)
print(dimensions[0])
print(dimensions[1])

# dimensions[0] = 250 是行不通的
# Traceback (most recent call last):
#   File "dimensions.py", line 2, in <module>
#     dimensions[0] = 250
# TypeError: 'tuple' object does not support item assignment

my_t = (3,)
# 严格来说元组是通过,来识别的，即时一个也要加逗号

for dimension in dimensions:
    print(dimension)

dimension = (200, 50)
print("Origianl dimensions:")
for dimension in dimensions:
    print(dimension)

dimensions = (400, 100)
print("Modified dimensions:")
for dimension in dimensions:
    print(dimension)
    