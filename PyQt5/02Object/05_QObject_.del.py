# 代码功能：演示QObject的删除机制
from PyQt5.Qt import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QObject的学习")
        self.resize(500, 500)
        self.setup_ui()

    def setup_ui(self):
        self.test_qobject_del()

    # 对象删除
    def test_qobject_del(self):
        obj1 = QObject()
        self.obj1 = obj1 # 保存obj1的引用，防止被删除
        obj2 = QObject()
        obj3 = QObject()

        obj3.setParent(obj2)
        obj2.setParent(obj1)

        obj1.destroyed.connect(lambda: print("obj1被删除"))
        obj2.destroyed.connect(lambda: print("obj2被删除"))
        obj3.destroyed.connect(lambda: print("obj3被删除"))

        # del obj2 # 手动删除obj2，会级联删除obj3
        obj2.deleteLater() # 异步删除obj2，不会级联删除obj3
        print(obj1.children()) # 查看obj1的子对象，发现obj2被删除了

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())