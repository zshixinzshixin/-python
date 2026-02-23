# 代码功能：展示抽象按钮的基本使用
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("QAbstractButton")
window.resize(500, 500)

class Btn(QAbstractButton):
    def paintEvent(self, evt): # 最基本的绘制按钮的方法，必须重写
        # print("绘制按钮")
        # 1. 创建画家对象
        painter = QPainter(self)

        # 2.设置画笔颜色和宽度
        # 方法1：先创建画笔对象，再设置画笔
        pen = QPen(QColor(111, 100, 50), 6)
        painter.setPen(pen)
        # 方法2：直接设置画笔
        # painter.setPen(QPen(Qt.red, 2))

        # 3. 绘制按钮
        # 3.1 绘制按钮的矩形框
        painter.drawRect(self.rect())
        # 3.2 绘制按钮的文本
        painter.drawText(self.rect(), Qt.AlignCenter, self.text()) # self.rect() 按钮的矩形框, Qt.AlignCenter 居中对齐, self.text() 按钮的文本
     
# btn = QAbstractButton(window) # 抽象按钮不能直接使用
btn = Btn(window)
btn.setText("按钮") # 设置按钮的文本为“按钮”

btn.pressed.connect(lambda: print("按钮被按下")) # 连接按钮的pressed信号到槽函数，槽函数打印“按钮被按下”
# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())