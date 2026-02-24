# 代码功能：展示命令链接按钮的基本使用
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("命令链接按钮")
window.resize(500, 500)

btn = QCommandLinkButton(window)
btn.setText("这里是按钮文本")
btn.setDescription("这里是按钮描述")
btn.move(100, 100)

print(btn.description())
# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())

