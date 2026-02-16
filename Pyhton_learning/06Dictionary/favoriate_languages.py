favorite_laguanges = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'rust',
    'phil': 'property'
}

language = favorite_laguanges['sarah'].title()
print(f"Sarch's favorite language is {language}")
# 这种语法用于获取任何人喜欢的语言

print('\n')
for name, language in favorite_laguanges.items():
    print(f"{name.title()}'s favorite language is {language.title()}.")
# 遍历语法，{}填写需要输出的变量内容（在f语句中）变量是从字典赋予的

print("\n")
for name in favorite_laguanges.keys():
    print(name.title())  
# 这里即使不用keys()也可以遍历键

print("\n")
friends = ['phil', 'sarah']
for name in favorite_laguanges.keys():
    print(f"Hi {name.title()}")
    
    if name in friends:
        language = favorite_laguanges[name].title()
        print(f"\t{name.title()}, I see you love {language}!")
# keys也能使用其中的值

if 'erin' not in favorite_laguanges.keys():
    print('\nerin, please take our poll!')
# keys其实返回的是列表，包含字典的所有键

print("\n")
for name in sorted(favorite_laguanges.keys()):
    print(f"{name.title()}, thank you for taking the poll.")

favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'rust',
    'phil': 'python',
    }
# 定义一个新的可重复的

print("The following languages have been mentioned:")
for language in favorite_languages.values():
    print(language.title())

print("\nThe following languages have been mentioned:")
for language in set(favorite_laguanges.values()):
    print(language.title())
# 这里用set设置为独一无二