first_name = "ada"
last_name = "lovelace"
full_name = f"{first_name} {last_name}" # 注意这上面中间加了空格，空格也会算进f字符串
print(full_name)

print(f"Hello,{full_name.title()}!")
message = f"Hello,{full_name.title()}!" # 使用f字符串创建消息，把消息赋给变量，最后print变量
print(message) 

print("Languages:\n\tPython\n\tC\n\tJavaScript")
# 这里利用\n\t,通过寥寥几行代码生成很多行输出

favorite_language = 'python '
print(favorite_language.rstrip())
print(favorite_language)
# 这里只是暂时删除了空白，如果要永久删除可以通过赋值完成
favorite_language = favorite_language.rstrip()
print(favorite_language)
# 还可以删除字符串左端的空白或同时删除字符串两端的空白
# 分别使用 lstrip() 方法和 strip() 方法即可

nostarch_url = 'https://nostarch.com'
print(nostarch_url.removeprefix('https://'))
