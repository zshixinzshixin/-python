# 代码功能：演示QWidget的内容边距
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
window = QWidget()
window.setWindowTitle("内容边距")
window.resize(500, 500)

label = QLabel(window)
label.setText("内容边距调整，更美观")
label.move(100, 100)
label.resize(300, 300)
label.setStyleSheet("background-color: red;")

label.setContentsMargins(50, 200, 0, 0) # 左,上,右,下

# 获取内容边距
print("contentsMargins",label.getContentsMargins()) 

window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())
