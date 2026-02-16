# 代码功能：演示QObject的信号机制
from PyQt5.Qt import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QObject的学习")
        self.resize(500, 500)
        self.setup_ui()
    def setup_ui(self):
        self.test_qobject_signal()

    def test_qobject_signal(self):
        self.obj = QObject()

        # 案例1:
        # def destroy_slot(obj): # 槽函数
        #     print("对象被销毁了", obj)
        
        # self.obj.destroyed.connect(destroy_slot) # 连接信号和槽函数

        # del self.obj # 手动销毁对象
        
        def obj_name_slot(name):
            print("对象的名称发生了改变", name)

        self.obj.objectNameChanged.connect(obj_name_slot)

        # self.obj.setObjectName("obj1")
        # self.obj.objectNameChanged.disconnect(obj_name_slot) # 断开信号和槽函数的连接
        # self.obj.setObjectName("obj2")

        # 测试: 阻塞信号后, .setName() 方法不会触发信号
        # self.obj.setObjectName("obj1")
        # self.obj.blockSignals(True) # 阻塞信号
        # self.obj.setObjectName("obj2")
        # self.obj.blockSignals(False) # 解除阻塞信号
        # self.obj.setObjectName("obj3")

        print(self.obj.receivers(self.obj.objectNameChanged)) # 查看信号的连接槽函数的数量


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())