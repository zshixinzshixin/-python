# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("工具按钮")
window.resize(500, 500)

tb = QToolButton(window)
tb.setText("这里是按钮文本")
tb.setIcon(QIcon("icon.ico")) 
# 默认显示图标，不显示文本
tb.setIconSize(QSize(64, 64))
tb.move(100, 100)

tb.setToolButtonStyle(Qt.ToolButtonTextBesideIcon) # 文本BesideIcon

tb2 = QToolButton(window)
tb2.setArrowType(Qt.DownArrow)
tb2.setText("下箭头")
tb2.move(100, 200)
tb2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 文本UnderIcon
print(tb2.arrowType()) # Qt.DownArrow
tb2.setAutoRaise(True)

# 需要长按才能生效
menu = QMenu(tb)

sub_menu = QMenu(menu)
sub_menu.setTitle("子菜单")
sub_menu.setIcon(QIcon("icon.ico"))

action = QAction(QIcon("icon.ico"), "动作", menu)
action.setData("123")
action.triggered.connect(lambda: print("动作被触发"))

menu.addAction(action)
menu.addSeparator()
menu.addMenu(sub_menu)

tb.setMenu(menu)

tb.setPopupMode(QToolButton.MenuButtonPopup) # 菜单按钮弹出


# ----- 信号 -----开始
def slot(act):
    print(act.text(), action.data())
tb.triggered.connect(slot)


# ----- 信号 -----结束
# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())