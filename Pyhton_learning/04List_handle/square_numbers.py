# 代码功能：演示列表的遍历和计算
squares = []
for value in range(1,11):
    square = value**2
    squares.append(square)
print(squares)

# 简化，不适用中间临时变量
squares = []
for value in range(1,11):
    squares.append(value**2)
print(squares)