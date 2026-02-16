prompt = "\nTell me something, and I will repeat it back to you:"
prompt += "\nEnter 'quit' to end the program."

message = ""
while message != 'quit':
    message = input(prompt)

    if message != 'quit':
        print(message)
# 这里输入quit直接结束程序（程序结束了）
# 多添加一个if语句防止结束程序还要继续打印