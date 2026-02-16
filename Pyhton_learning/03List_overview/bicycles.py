bicycles = ['trek', 'cannondale', 'redline', 'specialize'] # 汽车品牌
print(bicycles)

print(bicycles[0]) # 在 Python 中，第一个列表元素的索引为 0，而不是 1。
print(bicycles[0].title())

print(bicycles[1])
print(bicycles[3])

print(bicycles[-1])
# 用-1访问最后一个元素

message = f"My first bicycle was a {bicycles[0].title()}"
print(message)
# 你可以像使用其他变量一样使用列表中的各个值。