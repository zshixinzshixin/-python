# 案例1：点击按钮，数字加1
# 案例2：点击按钮，图标切换
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("按钮的文本提示和图标")
window.resize(500, 500)

# ----------文本提示----------开始
btn = QPushButton(window)
btn.setText("1")

def plus_one():
    print("push 1")
    num = int(btn.text()) + 1
    btn.setText(str(num))

btn.pressed.connect(plus_one)
# ----------文本提示----------结束

# ----------图标----------开始

btn.setIcon(QIcon("icon.ico")) # 设置图标
btn.setIconSize(QSize(50, 50)) # 设置图标大小

# ----------图标----------结束


# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())
