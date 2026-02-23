# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 方法1：窗口本身
class Window(QWidget):
    def contextMenuEvent(self, evt): # 上下文菜单事件
        print("contextMenuEvent 被调用")
        menu = QMenu(self)

        menu.addAction("1")
        menu.addAction("2")
        menu.addAction("3")
        menu.addAction("4")
        
        # point
        menu.exec_(evt.globalPos()) # 弹出菜单
        # menu.exec_(evt.pos())

        super().contextMenuEvent(evt) # 调用父类的方法


# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = Window()
# 2.2 设置控件
window.setWindowTitle("按钮信号")
window.resize(500, 500)

btn = QPushButton(window)
btn.setText("btn")
btn.move(150, 150)

def show_menu(point):
    # ------ 菜单 ------开始
    menu = QMenu(window)

    open_recent_menu = QMenu(menu)
    open_recent_menu.setTitle("最近打开")

    new_action = QAction(QIcon("icon.ico"), "新建", menu)
    new_action.triggered.connect(lambda: print("新建文件"))

    open_action = QAction(QIcon("icon.ico"), "打开", menu)
    open_action.triggered.connect(lambda: print("打开文件"))

    exit_action = QAction("退出", menu)
    exit_action.triggered.connect(lambda: print("退出程序"))

    file_action = QAction("Python-GUI编程-PyQt5")

    menu.addAction(new_action)
    menu.addAction(open_action)
    open_recent_menu.addAction(file_action)
    menu.addMenu(open_recent_menu)
    menu.addSeparator()
    menu.addAction(exit_action)
    # ------ 菜单 ------结束

    # point
    dest_point = window.mapToGlobal(point) # 3. 在槽函数里把局部坐标转成全局坐标
    menu.exec_(dest_point) # 4. 弹出菜单

# 方法2：自定义上下文菜单信号
window.setContextMenuPolicy(Qt.CustomContextMenu) # 1. 允许自定义上下文菜单
window.customContextMenuRequested.connect(show_menu) # 2. 把右键信号连到槽函数
# 注意：
# 窗口设置了 Qt.CustomContextMenuPolicy 并把右键信号连到了 show_menu 槽函数，
# Qt 就不会再调用默认的 contextMenuEvent()——因此里面的 print 永远不会执行。


# 2.3 展示控件
window.show()

# 3. 应用程序的执行, 进入到消息循环
sys.exit(app.exec_())