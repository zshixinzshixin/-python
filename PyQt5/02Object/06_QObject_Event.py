# 代码功能：演示QObject的事件处理机制
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

class App(QApplication):
    def notify(self, receiver, event):
        if receiver.inherits("QPushButton") and event.type() == QEvent.MouseButtonPress:
            print("全局级响应：按钮被点击了")
            # print(receiver, event)
        return super().notify(receiver, event) # 处理其他父类方法

class Btn(QPushButton):
    def event(self, event):
        if event.type() == QEvent.MouseButtonPress:
            print("控件级响应：按钮被点击了")
        return super().event(event)
    def mousePressEvent(self, event):
        print("具体事件级响应：按钮被点击了")
        return super().mousePressEvent(event) # 这里如果不写，就不会触发信号与槽机制

# 1. 创建一个应用程序对象
app = App(sys.argv)

# 2. 控件的操作
window = QWidget()

btn = Btn(window)
btn.setText("按钮")
btn.move(100, 100)

def slot():
    print("信号与槽机制：按钮被点击了")

btn.clicked.connect(slot)
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())