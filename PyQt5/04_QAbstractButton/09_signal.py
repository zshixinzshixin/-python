# 功能：演示 QPushButton 的可用信号
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("可用信号")
window.resize(500, 500)

class Btn(QPushButton):
    def hitButton(self, pos):
        center = QPoint(self.width() // 2, self.height() // 2)
        distance = QLineF(center, pos).length() 
        return distance <= self.width() / 2

    def paintEvent(self, event):
        super().paintEvent(event) # 先调用父类的 paintEvent 方法，绘制按钮的基本形状
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 6))
        # painter.drawEllipse(self.rect().center(), self.width() // 2, self.height() // 2)
        painter.drawEllipse(self.rect()) # 直接绘制矩形的内切圆
        
btn = Btn(window)
btn.setText("按钮")
btn.resize(200, 200)
btn.move(150, 150)
btn.setCheckable(True) # 设置按钮为可切换状态

btn.pressed.connect(lambda: print("按钮被按下了"))
btn.released.connect(lambda: print("按钮被释放了"))
btn.clicked.connect(lambda: print("按钮被点击了"))
btn.toggled.connect(lambda isChecked: print("按钮被切换了", isChecked))


# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())