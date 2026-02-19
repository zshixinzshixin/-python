# 代码功能：展示顶层窗口
# 案例：点击窗口最大化后，再次点击恢复正常状态
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

class Window(QWidget):
    def mousePressEvent(self, event):
        if self.isMaximized():
            self.showNormal() # 恢复正常展示窗口
        else:
            self.showMaximized() # 最大化展示窗口


# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = Window()
# 2.2 设置控件
window.resize(500, 500)

# icon = QIcon("icon.png") # 窗口图标
# window.setWindowIcon(icon) # 设置窗口图标
window.setWindowIcon(QIcon("icon.png")) # 直接设置窗口图标
print("窗口图标：", window.windowIcon()) # 打印窗口图标

window.setWindowTitle("顶层窗口") # 设置窗口标题，默认是python
print("窗口标题：", window.windowTitle()) # 打印窗口标题

window.setWindowOpacity(0.9) # 设置窗口透明度，0.0-1.0之间的浮点数
print("窗口透明度：", window.windowOpacity()) # 打印窗口透明度

print("窗口状态：", window.windowState() == Qt.WindowNoState) # 打印窗口状态是否是正常状态
# window.setWindowState(Qt.WindowMaximized) # 设置窗口状态为最大化


# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())