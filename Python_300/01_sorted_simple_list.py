'''
代码功能：展示sort()方法和sorted()函数的使用
需求：给一个简单的列表，对其元素进行排序
'''
# 原始列表
list1 = [20, 50, 10, 50, 30]

# sort(key = None, reverse = False)方法：对列表进行排序，直接修改原始列表。
# key(可选)：指定一个函数，该函数用于从每个元素中提取一个比较键。默认值为None，即直接比较元素本身。
# reverse(可选)：指定排序顺序。如果为True，则按降序排序；如果为False（默认值），则按升序排序。
list1.sort()
print(list1)
list1.sort(reverse=True)
print(list1)

# sorted(iterable, key=None, reverse=False)函数：返回一个新的已排序列表，而不修改原始列表。
# iterable：要排序的可迭代对象，例如列表、元组等。
# key(可选)：指定一个函数，该函数用于从每个元素中提取一个比较键。默认值为None，即直接比较元素本身。
# reverse(可选)：指定排序顺序。如果为True，则按降序排序；如果为False（默认值），则按升序排序。
list2 = sorted(list1)
print(list2)
list2 = sorted(list1, reverse=True)
print(list2)
