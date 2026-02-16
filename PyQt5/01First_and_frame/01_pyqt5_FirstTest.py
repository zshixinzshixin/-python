# 代码功能：演示PyQt5的第一个程序
import sys
from PyQt5.Qt import *

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("XXXXX")
window.resize(500,500)
window.move(400,200)

label = QLabel(window)
label.setText("Hello Qt")
label.move(200,200)

window.show()

sys.exit(app.exec_())