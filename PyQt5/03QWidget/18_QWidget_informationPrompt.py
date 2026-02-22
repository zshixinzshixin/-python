# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
# window = QWidget()
window = QMainWindow() # 组合控件
# 特点：懒加载：用到时才创建
# >>> 关键：给主窗口添加状态栏 <<<
status_bar = QStatusBar()
window.setStatusBar(status_bar)  

# 2.2 设置控件
window.setWindowTitle("信息提示案例") 
window.resize(500, 500)
window.setWindowFlags(Qt.WindowContextHelpButtonHint) # 隐藏帮助按钮

# 当鼠标停留在窗口控件上时，提示“这是一个窗口”
window.setToolTip("这是一个窗口")
print(window.toolTip()) # 这是一个窗口
window.setStatusTip("这是一个窗口")
print(window.statusTip()) # 这是一个窗口

window.setToolTipDuration(3000) # 3秒后自动消失, 0表示永久显示
print(window.toolTipDuration()) # 3000

label = QLabel(window)
label.setText("这是一个标签")
label.move(150, 200)
label.setStatusTip("这是一个标签")
label.setToolTip("这是一个标签")
print(label.statusTip()) # 这是一个标签



# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())