# 案例：
# 1.初始状态：文本框空、按钮置灰、标签隐藏
# 2.文本框有内容时按钮可用，否则置灰
# 3.文本框内容为 Sz 时点击按钮显示“登录成功”，否则显示“登录失败”
# 4.仅用 QLineEdit、QPushButton、QLabel 三个控件
# 5.信号用 textChanged，按钮状态用 setEnabled
from PyQt5.Qt import *


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("交互状态案例")
        self.resize(500, 500)
        self.setup_ui()

    def setup_ui(self):
        # 添加3个子控件，分别是标签、文本框和按钮
        label  = QLabel(self)
        label.setText("标签")
        label.move(150, 50)
        label.hide() # 隐藏标签

        le = QLineEdit(self)
        le.setText("输入框")
        le.move(150, 100)

        btn = QPushButton(self)
        btn.setText("按钮")
        btn.move(150, 150)
        btn.setEnabled(False) # 设置按钮为禁用状态
        
        def slot(text):
            print("文本内容发生改变", text)
            if len(text) > 0:
                btn.setEnabled(True)
            else:
                btn.setEnabled(False)
        le.textChanged.connect(slot)
        # 当文本框内容改变时，判断是否为空
        # le.textChanged.connect(lambda: btn.setEnabled(len(le.text()) > 0)) # 使用lambda表达式

        def slot2():
            if le.text() == "Sz":
                label.setText("登录成功")
                label.show()
            else:
                label.setText("登录失败")
                label.show()
        btn.clicked.connect(slot2)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())