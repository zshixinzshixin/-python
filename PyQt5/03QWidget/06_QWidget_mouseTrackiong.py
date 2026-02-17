# 代码功能：演示QWidget的鼠标跟踪
# 案例：label标签跟随鼠标移动
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("鼠标跟踪")
        self.resize(500, 500)
        self.setMouseTracking(True) # 开启鼠标跟踪

        # 自定义鼠标光标
        # pixmap = QPixmap("icon.png").scaled(30, 30)
        # cursor = QCursor(pixmap, 15, 15)
        # self.setCursor(cursor)
        
    def mouseMoveEvent(self, evt):
        print("mouseMoveEvent", evt.pos(), evt.globalPos()) # 窗口坐标, 全局坐标
        print(self.hasMouseTracking()) # 默认False

        label = self.findChild(QLabel)
        label.move(evt.pos()) # 鼠标跟踪，标签跟着移动
        # label.move(evt.localPos().x(), evt.localPos().y()) # 鼠标跟踪，标签跟着移动

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
window = MyWindow()


label = QLabel(window)
label.setText("这是一个标签")
label.move(100, 100)
label.setStyleSheet("background-color: cyan;")


window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())