# 0.导入需要的包和模块
from PyQt5.Qt import * # 主要包括了我们常用的一些类，汇总到一块
import sys

# 1.创建一个应用程序对象
app = QApplication(sys.argv)
# print(app.arguments())
# print(qApp.argumetns())
'''
args = sys.argv
print(args)
'''


# 2.控件的操作
# 创建控件，设置控件（大小，位置，样式...），事件，信号处理


# 3.应用程序的执行，进入到消息循环
# app.exec_() # 让整个程序开始执行，并进入消息循环（无线循环）,检测整个程序所接收到交互信息
sys.exit(app.exec_())






