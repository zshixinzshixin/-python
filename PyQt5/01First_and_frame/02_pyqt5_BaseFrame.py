# 0.导入需要的包和模块
from PyQt5.Qt import * # 主要包括了我们常用的一些类，汇总到一块
import sys

# 1.创建一个应用程序对象
# argv: 命令行参数列表
# args = sys.argv # 命令行参数列表, 第一个元素是脚本名称, 后面的元素是命令行参数, 可以为空, 也可以有多个
# print(args) # 打印命令行参数列表
# print(app.arguments()) # 打印命令行参数列表
app = QApplication(sys.argv)


# 2.控件的操作
# 创建控件，设置控件（大小，位置，样式...），事件，信号处理

# 2.1创建控件
# 当创建控件，如果该控件没有父控件，则为顶层控件（窗口）
# 系统会给窗口添加标题栏，窗口控件具备一些特性设置标题，图标
window = QWidget()
# window = QPushButtion()
# window = QLabel()

# 2.2设置控件
window.setWindowTitle("hello QT")
window.resize(400,400)
#window.setText("Hello qt")

# 控件可以作为容器（承载其他控件）
label = QLabel(window)
label.setText("xxx")
label.setWindowTitle("ABC")
label.move(100,50)

# 2.3展示控件
# 创建的控件不会被展示，只有主动调用show方法
window.show()

# 没有父控件，会有两个顶层窗口
# label.show()

# 3.应用程序的执行，进入到消息循环
# app.exec_() # 让整个程序开始执行，并进入消息循环（无线循环）,检测整个程序所接收到交互信息
# sys.exit() # 退出应用程序, 并返回一个状态码
sys.exit(app.exec_())

