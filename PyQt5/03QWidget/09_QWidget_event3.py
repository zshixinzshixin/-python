# 代码功能：演示事件消息的案例
# 案例1：鼠标进入标签，标签文字改变为“欢迎光临”，鼠标离开标签，标签文字改变为“谢谢惠顾”
# 案例2：键盘按下Tab键，标签文字改变为“Tab键按下了”，按下Ctrl+S键，标签文字改变为“Ctrl+S键按下了”，按下Ctrl+Shift+Z键，标签文字改变为“ctrl+Shift+Z键按下了”，其他键按下，标签文字改变为“其他键”
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

class MyLabel(QLabel):
    def enterEvent(self, evt):
        print("MyLabel：鼠标进入了标签")
        self.setText("欢迎光临")
    def leaveEvent(self, evt):
        print("MyLabel：鼠标离开标签")
        self.setText("谢谢惠顾")

    def keyPressEvent(self, evt):
        print("keyPressEvent：键盘按下了",end=" ")
        if evt.key() == Qt.Key_Tab:
            print("Tab键按下了")
        elif evt.modifiers() == Qt.ControlModifier and evt.key() == Qt.Key_S:
            print("Ctrl+S键按下了")
        elif evt.modifiers() == Qt.ShiftModifier | Qt.ControlModifier and evt.key() == Qt.Key_Z:
            print("ctrl+Shift+Z键按下了")
        else:
            print("其他键")
        
# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("鼠标操作案例")
window.resize(500, 500)

label = MyLabel(window)
label.resize(100, 50)
label.move(100, 100)
label.setStyleSheet("background-color: red;")
label.grabKeyboard() # 标签获取键盘焦点(※)



# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())