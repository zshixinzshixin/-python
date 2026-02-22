# 代码功能：演示QWidget的交互状态
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

class MyWindow(QWidget):
    def paintEvent(self, event):
        print("窗口被绘制了")
        return super().paintEvent(event)

class Btn(QPushButton):
    def paintEvent(self, event):
        print("按钮被绘制了")
        return super().paintEvent(event)

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = MyWindow()
# 2.2 设置控件
window.setWindowTitle("交互状态[*]") # 设置窗口标题为“交互状态[*]”，*表示窗口为修改状态
window.resize(500, 500)

window.setWindowModified(True) # 设置窗口为修改状态
print("窗口是否为修改状态：", window.isWindowModified()) # 打印窗口是否为修改状态

btn = Btn(window)
btn.setText("按钮")
btn.move(50, 50)
# btn.setEnabled(False) # 设置按钮为禁用状态
print("按钮是否启用：", btn.isEnabled()) # 打印按钮是否启用

def slot():
    print("按钮被点击了")
    btn.setVisible(False) # 隐藏按钮
    
    print("按钮是否可见：", btn.isVisible()) # 打印按钮是否可见
    print("按钮是否隐藏：", btn.isHidden()) # 打印按钮是否隐藏
    print("按钮是否对窗口可见：", btn.isVisibleTo(window)) # 打印按钮是否对窗口可见

btn.clicked.connect(slot) # 连接信号和槽函数

w2 = QWidget()
w2.setWindowTitle("子窗口")
w2.show() # 展示子窗口

# 2.3 展示控件
window.setVisible(True)
# window.show() # 只是上面的函数的一种展示方式

# window.setVisible(False) # 隐藏窗口
# window.setHidden(True) # 设置窗口为隐藏状态
# window.hide() # 隐藏窗口
# window.close() # 关闭窗口

# w2.raise_() #  提升子窗口到顶部

print("子窗口是否为活动窗口：", w2.isActiveWindow()) # 打印子窗口是否为活动窗口

w2.close() # 关闭子窗口
# w2.setAttribute(Qt.WA_DeleteOnClose, True) # 设置子窗口关闭时删除对象
# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())