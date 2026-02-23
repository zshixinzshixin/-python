# 功能：演示 QPushButton 的创建和菜单
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("创建按钮和菜单")
window.resize(500, 500)

btn = QPushButton(window, text="按钮", icon=QIcon("icon.ico"))
btn.move(150, 150)

# ------ 菜单 ------开始
# 创建菜单
menu = QMenu()
open_all_menu = QMenu("全部打开", menu)

# 子菜单
newAction = QAction("新动作", menu)
newAction.setIcon(QIcon("icon.ico"))
# newAction = QAction("新动作", menu, QIcon("icon.ico")) # 合并操作
menu.addAction(newAction)
newAction.triggered.connect(lambda: print("新动作被触发"))

menu.addSeparator()  # 分割线

menu.addMenu(open_all_menu)
newAction = QAction("啥玩意")
open_all_menu.addAction(newAction)

menu.addSeparator()  # 分割线

menu.addAction("打开")
menu.addAction("保存")
menu.addAction("退出")

# 设置菜单
btn.setMenu(menu)

# ------ 菜单 ------结束

# 2.3 展示控件
window.show()
# btn.showMenu() # 点击按钮显示菜单

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())