# 这里首先从 pathlib 模块导入 Path 类。
# Path 对象指向一个文件，可用来做很多事情。
# 例如，让你在使用文件前核实它是否存在，读取文件的内容，以及将新数据写入文件。
from pathlib import Path

path = Path('pi_digits.txt')
contents = path.read_text().rstrip()
# method chaining 方法链式调用
print(contents)

print("--------")
contents = path.read_text()
lines = contents.splitlines()
# splitlines返回一个列表，包含每一行内容。
for line in lines:
    print(line)