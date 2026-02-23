# 代码功能：演示快捷键功能
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("快捷键")
window.resize(500, 500)

btn = QPushButton(window)
btn.pressed.connect(lambda: print("press"))
btn.setText("a&bc")
# 界面上 不显示 & 本身，而是把紧随其后的字母 b 加上下划线，提示用户：
# Alt + b 即可触发该按钮，相当于鼠标点击。
# 只有 第一个 & 生效；若文本里需要真正的 &，用 && 转义。
btn.setShortcut("Ctrl+T") # 快捷键：Ctrl+t

# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())