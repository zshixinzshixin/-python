# 代码功能：演示自动重复功能
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("自动重复")
window.resize(500, 500)

btn = QPushButton(window)
btn.setText("重复")
print(btn.autoRepeat()) # False

btn.setAutoRepeat(True) # 自动重复
btn.setAutoRepeatDelay(500) # 自动重复延迟时间：500ms
btn.setAutoRepeatInterval(200) # 自动重复间隔时间：200ms

print(btn.autoRepeat()) # True
print(btn.autoRepeatDelay()) # 500
print(btn.autoRepeatInterval()) # 200

btn.pressed.connect(lambda: print("press"))

# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())