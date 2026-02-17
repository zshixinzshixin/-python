# 代码功能：演示QWidget的事件消息
from PyQt5.Qt import *


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("事件消息的学习")
        self.resize(500, 500)
        self.setup_ui()

    def setup_ui(self):
        pass

    def showEvent(self, evt):
        print("showEvent：窗口被展示了")
    def hideEvent(self, evt):
        print("hideEvent：窗口被隐藏了")
    def moveEvent(self, evt):
        print("moveEvent：窗口被移动了")
    def resizeEvent(self, evt):
        print("resizeEvent：窗口被调整了大小")
    def enterEvent(self, evt):
        print("enterEvent：鼠标进入了窗口")
        self.setStyleSheet("background-color: red;")
    def leaveEvent(self, evt):
        print("leaveEvent：鼠标离开窗口")
        self.setStyleSheet("background-color: green;")
    def mousePressEvent(self, evt):
        print("mousePressEvent：鼠标按下了")
        if evt.button() == Qt.LeftButton:
            print("左键按下了")
        elif evt.button() == Qt.RightButton:
            print("右键按下了")
        elif evt.button() == Qt.MidButton:
            print("中键按下了")
    def mouseReleaseEvent(self, evt):
        print("mouseReleaseEvent：鼠标释放了")
        if evt.button() == Qt.LeftButton:
            print("左键释放了")
        elif evt.button() == Qt.RightButton:
            print("右键释放了")
        elif evt.button() == Qt.MidButton:
            print("中键释放了")
    def mouseDoubleClickEvent(self, evt):
        print("mouseDoubleClickEvent：鼠标双击了")

    def mouseMoveEvent(self, evt):
        print("mouseMoveEvent：鼠标移动了",end="")
        print("pos:", evt.pos())
    def keyPressEvent(self, evt):
        print("keyPressEvent：键盘按下了",end=" ")
        if evt.key() == Qt.Key_Up:
            print("上")
        elif evt.key() == Qt.Key_Down:
            print("下")
        elif evt.key() == Qt.Key_Left:
            print("左")
        elif evt.key() == Qt.Key_Right:
            print("右")
        elif evt.key() == Qt.Key_Enter:
            print("回车")
        elif evt.key() == Qt.Key_Space:
            print("空格")
        else:
            print("其他键")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())