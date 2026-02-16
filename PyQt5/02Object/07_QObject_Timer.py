# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

class MyObject(QObject):
    def __init__(self):
        super().__init__()
        self.timerId = self.startTimer(1000) # 1000ms 触发一次定时器事件
    def timerEvent(self, event):
        if event.timerId() == self.timerId:
            print("定时器事件触发了")

class MyLabel(QLabel):
    def __init__(self, *argv, **kargs):
        super().__init__(*argv, **kargs) # 调用父类的构造函数
        self.setText("10")
        self.setStyleSheet("font-size: 25px; color: red;")

    def setSec(self, sec): # 设置倒计时的秒数
        self.setText(str(sec))

    def startCountdown(self, ms): # 开始倒计时
        self.timerId = self.startTimer(ms) # ms 触发一次定时器事件

    def timerEvent(self, *argv, **kargs):
        current_sec = int(self.text())
        next_sec = current_sec - 1
        self.setText(str(next_sec))
        if next_sec <= 0:
            self.killTimer(self.timerId)
            self.setText("倒计时结束")


# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("Qobject定时器的使用")
window.resize(500, 500)

obj = MyObject()

label = MyLabel(window)
label.move(100, 100)
label.setSec(5) # 倒计时5秒,调用setSec方法
label.startCountdown(1000) # 开始倒计时,调用startCountdown方法


# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())