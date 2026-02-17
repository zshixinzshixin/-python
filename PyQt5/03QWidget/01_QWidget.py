# 代码功能：演示QWidget的使用和继承关系
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("QWidget学习")
window.resize(500, 500)

# print(QWidget.__bases__) # 显示QWidget的直接父类
print(QWidget.mro()) # 显示QWidget的继承关系
# print(QWidget.__subclasses__()) # 显示QWidget的直接子类

red = QWidget(window)
red.setStyleSheet("background-color: red;")
red.resize(100, 100)
red.move(150, 150)

green = QWidget(window)
green.setStyleSheet("background-color: green;")
green.resize(100, 100)
green.move(200, 200)

# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())