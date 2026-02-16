from PyQt5.Qt import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QObject的学习")
        self.resize(500, 500)
        self.setup_ui()

    def setup_ui(self):
        self.test_qobject_type()

    # 类型判定
    def test_qobject_type(self):
        obj = QObject()
        w = QWidget()
        btn = QPushButton()
        label = QLabel()

        objs = [obj, w, btn, label]
        for o in objs:
            print(o.isWidgetType(), end = " ") # 判定是否是控件类型
            print(o.inherits("QWidget")) # 判定是否是QWidget的子类


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())