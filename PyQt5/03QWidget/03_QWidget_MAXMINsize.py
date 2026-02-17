# 代码功能：演示QWidget的最小尺寸最大尺寸限定
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("最小尺寸最大尺寸限定")
window.resize(500, 500) # 可改变尺寸
# window.setFixedSize(500, 500) # 固定尺寸，不能改变
window.setMinimumSize(300, 300) # 最小尺寸
window.setMaximumSize(800, 800) # 最大尺寸
print("minimumSize",window.minimumSize()) # QSize(300, 300)
print("maximumSize",window.maximumSize()) # QSize(800, 800)

window.resize(2000, 2000) # 超出最大尺寸，会被限定为最大尺寸
print("geometry",window.geometry()) # QRect(300, 300, 800, 800)

# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())