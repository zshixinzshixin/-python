# 代码功能：展示层级关系调整（同级控件）
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("层级关系调整")
window.resize(500, 500)

label1 = QLabel(window)
label1.setText("标签1")
label1.resize(100, 100)
label1.setStyleSheet("background-color: red;")

label2 = QLabel(window)
label2.setText("标签2")
label2.resize(100, 100)
label2.move(50, 50) # 遮挡部分，标签2在标签1的下方
label2.setStyleSheet("background-color: blue;")

label1.raise_() # 提升层级，标签1在标签2的上方
label2.lower() # 降低层级，标签2在标签1的下方
label2.stackUnder(label1) # 标签2在标签1的下方

# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())