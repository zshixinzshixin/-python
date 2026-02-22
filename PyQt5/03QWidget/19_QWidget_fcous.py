# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

class Window(QWidget):
    def mousePressEvent(self, evt):
        self.focusNextChild() # 切换到下一个子控件
        QWidget.setTabOrder(le1, le2) # 设置Tab键切换顺序
        QWidget.setTabOrder(le2, le3)

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
window = Window()

window.setWindowTitle("焦点控制")
window.resize(500, 500)

le1 = QLineEdit(window)
le1.move(150, 50)

le2 = QLineEdit(window)
le2.move(150, 100)

le3 = QLineEdit(window)
le3.move(150, 150)

le2.setFocus() # 使le2获得焦点,按Tab键切换
le2.setFocusPolicy(Qt.TabFocus) # 只能通过Tab键获得焦点, 不能通过点击获得焦点
le3.setFocusPolicy(Qt.StrongFocus) # 可通过Tab键和点击获得焦点

le2.clearFocus() # 清除焦点

window.show()

# 获取当前窗口内部，所有子控件获取焦点那个控件
print(window.focusWidget())

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())