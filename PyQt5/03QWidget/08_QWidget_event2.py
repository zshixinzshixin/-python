# 代码功能：演示事件转发
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

class Window(QWidget):
    def mousePressEvent(self, evt):
        print("Window：鼠标按下了")

class MidWidget(QWidget):
    def mousePressEvent(self, evt):
        print("MidWidget：鼠标按下了")

class Label(QLabel):
    pass # 不处理，事件转发给父控件（※）
    # def mousePressEvent(self, evt):
    #     print("Label：鼠标按下了")
    #     evt.ignore() # 忽略事件，事件转发给父控件
    #     evt.accept() # 接受事件，事件不转发给父控件
    #     evt.setAccepted(False) # 忽略事件，事件转发给父控件
        

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = Window()
# 2.2 设置控件
window.setWindowTitle("事件转发")
window.resize(500, 500)

mid_window = MidWidget(window)
mid_window.move(100, 100)
mid_window.resize(200, 200)
mid_window.setAttribute(Qt.WA_StyledBackground, True) # 作用：开启样式表
mid_window.setStyleSheet("background-color: yellow;")

label = Label(mid_window)
label.move(50, 50)
label.setText("这是一个标签")
label.setStyleSheet("background-color: red;")



# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())