# 代码功能：演示QObject的基本操作，包括继承关系、父对象、子对象、属性
from PyQt5.Qt import *

def QtFindChildrenRecursively(obj):
    """递归查找QObject的所有子对象"""
    children = []
    for child in obj.children():
        children.append(child)
        children.extend(QtFindChildrenRecursively(child))
    return children


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QObject的学习")
        self.resize(500, 500)
        self.setup_ui()
    def setup_ui(self):
        # self.test_qobject_inheritance
        # self.test_qobject_API()
        self.test_qobject_parent_and_child()
    
    # qobject的继承关系
    def test_qobject_inheritance(self):
        mros = QObject.mro() # 获取QObject的所有父类
        for mro in mros: # 打印QObject的所有父类
            print(mro)
    
    # QObject对象名称和属性的操作
    def test_qobject_API(self):
        # ---------- 测试API ----------开始
        # 测试QObject对象的名称
        # obj = QObject()
        # obj.setObjectName("my_object")
        # print(obj.objectName())

        # 测试QObject对象的属性
        # obj.setProperty("my_property", "error")
        # obj.setProperty("my_property2", "error2")
        # print(obj.property("my_property"))
        # print(obj.property("my_property2"))

        # 测试QObject对象的动态属性
        # print(obj.dynamicPropertyNames())
        # ---------- 测试API ----------结束

        # ----------案例演示 ----------开始
        # 从文件中读取QSS样式表, 并应用到应用程序
        with open("QObject.qss", "r", encoding="utf-8") as f:
            qApp.setStyleSheet(f.read())
        
        label = QLabel(self) # 创建一个标签控件
        label.setObjectName("notice") # 设置标签的对象名称, 用于QSS样式表中选择器的匹配
        label.setProperty("notice_level", "nomal") # 设置标签的属性值, 用于QSS样式表中属性选择器的匹配
        label.setText("这是一个正常标签") # 设置标签的文本内容
        label.move(100, 100) # 移动标签的位置

        label2 = QLabel(self) # 创建一个标签控件
        label2.setObjectName("notice") # 设置标签的对象名称, 用于QSS样式表中选择器的匹配
        label2.setProperty("notice_level", "warning") # 设置标签的属性值, 用于QSS样式表中属性选择器的匹配
        label2.setText("这是一个警告标签") # 设置标签的文本内容
        label2.move(100, 200) # 移动标签的位置

        
        label3 = QLabel(self) # 创建一个标签控件
        label3.setObjectName("notice") # 设置标签的对象名称, 用于QSS样式表中选择器的匹配
        label3.setProperty("notice_level", "error") # 设置标签的属性值, 用于QSS样式表中属性选择器的匹配
        label3.setText("这是一个错误标签") # 设置标签的文本内容
        label3.move(100, 300) # 移动标签的位置

        # 这里字体样式不会生效, 因为按钮控件的类名是QPushButton, 而不是QLabel
        btn = QPushButton(self) # 创建一个按钮控件
        btn.setText("这是一个按钮") # 设置按钮的文本内容
        btn.move(100, 400) # 移动按钮的位置
        # ----------案例演示 ----------结束

    # QObject对象的父子关系操作
    def test_qobject_parent_and_child(self):
        # ---------- 测试QObject API ----------开始
        # obj1 = QObject()
        # obj2 = QObject()
        # obj3 = QObject()
        # print('obj1', obj1)
        # print('obj2', obj2)

        # obj1.setParent(obj2) # 设置obj1的父对象为obj2
        # obj3.setParent(obj1) # 设置obj3的父对象为obj1
        # print(obj1.parent())
        # print(obj2.children())
        
        # print(QtFindChildrenRecursively(obj2)) # 递归查找obj2的所有子对象
        # ---------- 测试QObject API ----------结束
        # ----------内存管理机制 ----------开始
        obj1 = QObject()
        self.obj1 = obj1
        obj2 = QObject()

        obj2.setParent(obj1) # 设置obj2的父对象为obj1

        del obj1 # 删除obj1对象, 会导致obj2对象被释放

        # 监听obj2对象被释放
        obj2.destroyed.connect(lambda: print("obj2被释放了"))

        # ----------内存管理 ----------结束


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())