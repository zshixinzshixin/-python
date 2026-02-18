# 代码功能：学习QWidget的父子关系
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("父子关系学习")
window.resize(500, 500)

label1 = QLabel(window)
label1.setText("标签1")
label1.move(100, 100)

label2 = QLabel(window)
label2.setText("标签2")
label2.move(100, 200)

label3 = QLabel(window)
label3.setText("标签3")
label3.move(100, 300)

print(window.childAt(55, 55)) # None
print(window.childAt(100, 100)) # <PyQt5.QtWidgets.QLabel object at 0x0000020D00000048>

print(label2.parentWidget()) # <PyQt5.QtWidgets.QWidget object at 0x0000020D00000048>
print(label2.parent()) # <PyQt5.QtWidgets.QWidget object at 0x0000020D00000048>

print(window.childrenRect()) # PyQt5.QtCore.QRect(100, 100, 100, 230)
# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())