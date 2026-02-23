# 0. 导入需要的包和模块
from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2. 控件的操作
# 2.1 创建控件
window = QWidget()
# 2.2 设置控件
window.setWindowTitle("窗口标题")
window.resize(500, 500)

pushBtn = QPushButton(window)
pushBtn.setText("按钮")
pushBtn.move(100, 100)

radioBtn = QRadioButton(window)
radioBtn.setText("单选框")
radioBtn.move(100, 200)

checkBox = QCheckBox(window)
checkBox.setText("复选框")
checkBox.move(100, 300)

radioBtn.setStyleSheet("QRadioButton:checked{background-color: red;}") # 单选框被选中时背景颜色为红色

# 把3个按钮都置于按下状态
pushBtn.setDown(True)
radioBtn.setChecked(True)
checkBox.setChecked(True)

# 是否可被选中
print(pushBtn.isCheckable()) # False
print(radioBtn.isCheckable()) # True
print(checkBox.isCheckable()) # True

# 是否被选中
print(pushBtn.isChecked()) # False
print(radioBtn.isChecked()) # True
print(checkBox.isChecked()) # True

# 切换按钮状态
btn = QPushButton(window)
btn.setText("切换")
btn.move(100, 400)
def slot():
    pushBtn.toggle()
    # 等效于
    # pushBtn.setDown(not pushBtn.isDown())
    radioBtn.toggle()
    checkBox.toggle()
btn.clicked.connect(slot)

# pushBtn.setEnabled(False) # 禁用按钮

# 2.3 展示控件
window.show()

# 3. 应用程序的执行，进入到消息循环
sys.exit(app.exec_())