# 案例：创建一个顶层窗口·要求
# 1.无边框无标题栏
# 2.窗口半透明
# 3.自定义最小化，最大化，关闭按钮
# 4.支持拖拽用户区移动

# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(Qt.FramelessWindowHint) # 方法2：设置控件为无边框无标题栏

        self.setWindowOpacity(0.9) # 设置窗口半透明
        self.setWindowTitle("顶层窗口案例")
        self.resize(500, 500)

    

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# window = QWidget(falgs=Qt.FramelessWindowHint) # 方法1：创建控件时设置无边框无标题栏
window = Window()

# 添加3个按钮：自定义最小化，最大化，关闭按钮
top_margin = 10 # 按钮的顶部间距
# 关闭按钮
# close_btn = QPushButton("关闭", window) # 方法1：创建按钮时设置文本
close_btn = QPushButton(window) 
close_btn.setText("关闭") # 方法2：创建按钮后设置按钮文本
close_btn_w = close_btn.width()
window_w = window.width()
close_btn.move(window_w - close_btn_w, top_margin)

# 最大化按钮
max_btn = QPushButton(window)
max_btn.setText("最大化")
max_btn_w = max_btn.width()
max_btn.move(window_w - max_btn_w - close_btn_w, top_margin)

# 最小化按钮
min_btn = QPushButton(window)
min_btn.setText("最小化")
min_btn_w = min_btn.width()
min_btn.move(window_w - min_btn_w - close_btn_w - max_btn_w, top_margin)

# slot：槽函数，响应信号
# def close_window():
#     window.close()
def maximize_window():
    if window.isMaximized():
        window.showNormal()
        max_btn.setText("最大化")
    else:
        window.showMaximized()
        max_btn.setText("正常")
def minimize_window():
    window.showMinimized()

# 监听信号
# close_btn.clicked.connect(close_window) # 方法1：使用槽函数
close_btn.clicked.connect(lambda: window.close()) # 方法2：使用lambda表达式
max_btn.clicked.connect(maximize_window)
min_btn.clicked.connect(minimize_window)

window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())