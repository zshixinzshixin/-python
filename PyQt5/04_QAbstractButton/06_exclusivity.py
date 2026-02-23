# 代码功能：演示按钮控件的排他性
# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("排他性")
window.resize(500, 500)

for i in range(3):
    radioBtn = QRadioButton(window)
    radioBtn.setText(f"单选框{i}")
    radioBtn.move(100, 200 + i * 50)

    # 默认情况下，单选框是排他性的，按钮和复选框是非排他性的
    # radioBtn.setAutoExclusive(False) # 设置为非排他性
    radioBtn.setAutoExclusive(True) # 设置为排他性
    radioBtn.setChecked(i == 0) # 第一个单选框默认被选中

# 排他性基于相同的父对象
radio4 = QRadioButton(window)
radio4.setText("单选框4")
radio4.move(100, 300)
radio4.setCheckable(True) # 第二个单选框默认被选中

# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())