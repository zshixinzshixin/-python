# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("模拟点击")
window.resize(500, 500)

btn = QPushButton(window)
btn.setText("按钮")
btn.move(100, 100)

btn.clicked.connect(lambda: print("按钮被点击了"))

# 模拟点击按钮
btn.click() # 普通点击
btn.animateClick() # 模拟点击按钮，会有动画效果


# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())