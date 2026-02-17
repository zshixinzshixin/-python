# 代码功能：演示QWidget的大小和位置
# 案例：在一个窗口中，创建20个红色的控件，每个控件的大小为100x100，
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys


# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 设置控件

window = QWidget()
window.resize(500, 500)
window.move(300, 300)

print("x",window.x()) # 100
print("y",window.y()) # 100
print("height",window.height()) # 200
print("width",window.width()) # 200
print("pos",window.pos()) # QPoint(100, 100)
print("geometry",window.geometry()) # QRect(100, 100, 200, 200)

# 总的控剑数
widget_count = 20
# 列数
column_count = 4
# 行数（向上取整）
row_count = (widget_count-1) // column_count + 1
# 计算一个控件的宽度
widget_width = window.width() // column_count
# 计算一个控件的高度
widget_height = window.height() // row_count

for i in range(widget_count):
    w = QWidget(window)
    w.resize(widget_width, widget_height)
    w.setStyleSheet("background-color: red;border: 1px solid black;") # 边框为1px，颜色为黑色
    w.move((i % column_count) * widget_width, (i // column_count) * widget_height)

window.show()


# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())