# 代码功能：演示文本框的使用
# 案例：复制
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("QLineEdit 功能测试")
window.resize(500, 500)

le_a = QLineEdit(window)
le_a.move(100, 100)
le_a.resize(200, 30)

le_b = QLineEdit(window)
le_b.move(100, 200)
le_b.resize(200, 30)

copy_btn = QPushButton("复制", window)
copy_btn.move(100, 300)

def copy():
    le_b.setText(le_a.text())

copy_btn.clicked.connect(copy)


# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())