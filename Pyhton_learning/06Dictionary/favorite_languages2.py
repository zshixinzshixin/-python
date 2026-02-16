favorite_laguanges = {
    'jen': ['python', 'rust'],
    'sarah': ['c'],
    'edward': ['rust', 'go'],
    'phil': ['python', 'haskell'],
}

for name, languages in favorite_laguanges.items():
    print(f"\n{name.title()}'s favoriate languages are:")
    for language in languages:
        print(f"\t{language.title()}")

# 字典里嵌套列表然后通过循环输出
# 这里可以再优化一下

print(".......")
for name, languages in favorite_laguanges.items():
    if len(favorite_laguanges[name]) == 1:
        print(f"\n{name.title()}'s favoriate languages is {languages[0].title()}")
    else:
        print(f"\n{name.title()}'s favoriate languages are:")
        for language in languages:
            print(f"\t{language.title()}")
#  {languages[0].title()} 这一步是为了不输出为列表