# 代码功能：演示单选按钮的使用
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("单选按钮")
window.resize(500, 500)

red = QWidget(window)
red.resize(200, 200)
red.move(50, 50)
red.setStyleSheet("background-color:red")
green = QWidget(window)
green.resize(200, 200)
green.move(red.x()+red.width(), red.y()+red.height())
green.setStyleSheet("background-color:green")

rb_boy = QRadioButton("男-&Boy", red)
rb_boy.setShortcut("Alt+B")
rb_boy.move(10, 10)
rb_girl = QRadioButton("女-&Girl", red)
rb_girl.setShortcut("Alt+G")
rb_girl.move(10, 50)

# 信号：toggled(checked)
rb_girl.toggled.connect(lambda: print("女被选中了吗？", rb_girl.isChecked()))

rb_no = QRadioButton("无", green)
rb_no.move(10, 10)
rb_yes = QRadioButton("有", green)
rb_yes.move(10, 50)

# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())