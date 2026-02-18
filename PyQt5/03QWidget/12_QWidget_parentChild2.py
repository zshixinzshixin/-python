# 案例：通过父子关系，实现点击标签，标签背景颜色变红
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 方法1：直接在窗口中处理鼠标点击事件
# class Label(QLabel):
#     def mousePressEvent(self, evt):
#         self.setStyleSheet("background-color: red;")

# 方法2：在窗口中处理鼠标点击事件，判断点击到了哪个子控件
class Window(QWidget):
    def mousePressEvent(self, evt):
        local_x = evt.x()
        local_y = evt.y()
        print("窗口被点击了", local_x, local_y)
        sub_widget = self.childAt(local_x, local_y)
        if sub_widget and isinstance(sub_widget, QLabel): # 点击到了标签
            sub_widget.setStyleSheet("background-color: red;")



# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = Window()
# 2.2 设置控件
window.setWindowTitle("父子关系案例")
window.resize(500, 500)

for i in range(10):
    label = QLabel(window)
    label.setText(f"标签{i}")
    label.move(40 * i, 100 + i * 30)

# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())