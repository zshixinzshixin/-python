# 代码功能：展示按钮的有效区域（点击按钮的有效区域为按钮的内切圆）
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("设置有效区域")
window.resize(500, 500)

class Btn(QPushButton):
    def hitButton(self, pos):

        # if pos.x() > self.width() / 2: # 点击按钮右边区域才有效
        #     return True
        # else:
        #     return False # 点击区域不在按钮有效区域内
        
        # 通过给定一个点坐标，计算与圆心的距离

        center = QPoint(self.width() // 2, self.height() // 2)
        # 注意：QPoint 的构造函数只接受 整数，而 self.width()/2 得到的是 float，
        # 于是爆出了 unexpected type 'float'。把坐标先转成 int（或直接用 // 整除）即可

        # 方法1：QLineF 自带长度
        distance = QLineF(center, pos).length() 
        # 方法2：math.hypot
        # distance = math.hypot(point.x() - center.x(), point.y() - center.y())

        return distance <= self.width() / 2
        # 如果点击区域在按钮有效区域内，返回 True，否则返回 False

    def paintEvent(self, event):
        super().paintEvent(event) # 先调用父类的 paintEvent 方法，绘制按钮的基本形状
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 6))
        painter.drawEllipse(self.rect().center(), self.width() // 2, self.height() // 2)
        # painter.drawEllipse(self.rect()) # 直接绘制矩形的内切圆
        
btn = Btn(window)
btn.setText("按钮")
btn.resize(200, 200)
btn.move(150, 150)

btn.pressed.connect(lambda: print("按钮被按下了"))

# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())