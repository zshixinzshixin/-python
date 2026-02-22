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
        super().__init__(*args, **kwargs) # 调用父类的构造方法，创建控件
        self.setWindowFlags(Qt.FramelessWindowHint) # 方法2：设置控件为无边框无标题栏

        self.setWindowOpacity(0.9) # 设置窗口半透明
        self.setWindowTitle("顶层窗口案例")
        self.resize(500, 500)

        # 公共属性
        self.top_margin = 10 # 按钮的顶部间距
        self.btn_w = 80 # 按钮的宽度
        self.btn_h = 40 # 按钮的高度

        # 用于拖拽的变量
        self.moving = False # 记录是否正在移动窗口
        self.move_pos = QPoint() # 记录移动的位置

        self.setup_ui()

    def setup_ui(self): 
        # 添加3个按钮：自定义最小化，最大化，关闭按钮
        # 关闭按钮
        # close_btn = QPushButton("关闭", self) # 方法1：创建按钮时设置文本
        close_btn = QPushButton(self) 
        self.close_btn = close_btn # 将close_btn赋值给self.close_btn
        close_btn.setText("关闭") # 方法2：创建按钮后设置文本
        close_btn.resize(self.btn_w, self.btn_h) # 设置按钮的大小

        # 最大化按钮
        max_btn = QPushButton(self)
        self.max_btn = max_btn # 将max_btn赋值给self.max_btn
        max_btn.setText("最大化")
        max_btn.resize(self.btn_w, self.btn_h) # 设置按钮的大小

        # 最小化按钮
        min_btn = QPushButton(self)
        self.min_btn = min_btn # 将min_btn赋值给self.min_btn
        min_btn.setText("最小化")
        min_btn.resize(self.btn_w, self.btn_h) # 设置按钮的大小
    
        # slot：槽函数，响应信号
        # def close_window():
        #     window.close()
        def maximize_window():
            if self.isMaximized():
                self.showNormal()
                max_btn.setText("最大化")
            else:
                self.showMaximized()
                max_btn.setText("正常")
        def minimize_window():
            self.showMinimized()

        # 连接信号
        # close_btn.clicked.connect(close_window) # 方法1：使用槽函数
        close_btn.clicked.connect(lambda:self.close()) # 方法2：使用lambda表达式
        max_btn.clicked.connect(maximize_window)
        min_btn.clicked.connect(minimize_window)
        
    def resizeEvent(self, event):

        # 当窗口大小改变时，更新按钮的位置
        window_w = self.width()
        # 关闭按钮（最右边）
        self.close_btn.move(window_w - self.btn_w - 10, self.top_margin)
        # 最大化按钮
        self.max_btn.move(window_w - self.btn_w * 2 - 15, self.top_margin)
        # 最小化按钮
        self.min_btn.move(window_w - self.btn_w * 3 - 20, self.top_margin)

    
    # 局部坐标转换法（用鼠标在窗口内的相对位移，去叠加窗口在屏幕上的绝对位置）
    # （除此之外，还可以使用全局坐标转换法、框架几何法）
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moving = True # 记录是否正在移动窗口
            self.move_pos = event.pos() # 鼠标相对位置（鼠标相对于当前窗口客户区的位置）这里相当于移动起点位置
            event.accept()
    def mouseMoveEvent(self, event):
        if self.moving:
            self.move(self.pos() + event.pos() - self.move_pos) 
            # 移动窗口 = 当前窗口位置（相对于左上角坐标） + 鼠标相对位置 - 移动起点位置
            event.accept()
    def mouseReleaseEvent(self, event):
        self.moving = False # 记录是否正在移动窗口
        event.accept()

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# window = QWidget(falgs=Qt.FramelessWindowHint) # 方法1：创建控件时设置无边框无标题栏
window = Window()

window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())