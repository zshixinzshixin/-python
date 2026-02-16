def build_profile(first, last, **user_info):
    """"创建一个字典其中包含我们知道的关于用户的一切"""
    user_info['first name'] = first
    user_info['last name'] = last
    return user_info

user_profile = build_profile('albert', 'einstein', Location='princeton', field='physics')
print(user_profile)
# 接受任意数量的关键字实参
