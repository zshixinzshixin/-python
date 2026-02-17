# 代码功能：演示QWidget的鼠标形状，自定义鼠标形状，取消自定义鼠标形状
# 0. 导入需要的包和模块 
from PyQt5.Qt import * 
import sys 
import os


# 1. 创建一个应用程序对象 
app = QApplication(sys.argv) 


# 2. 控件的操作 
window = QWidget() 
window.setWindowTitle("鼠标形状") 
window.resize(500, 500) 


# window.setCursor(Qt.BusyCursor) # 繁忙光标 
window.setCursor(Qt.PointingHandCursor) # 指针手光标 


label = QLabel(window) 
label.setText("自定义鼠标形状") 
label.move(100, 100) 
label.resize(300, 300) 
label.setStyleSheet("background-color: cyan;") 


# 尝试加载自定义鼠标图片
current_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(current_dir, "icon.png")

pixmap = QPixmap(icon_path)
if pixmap.isNull():
    print(f"警告：无法加载图片 {icon_path}")
    print("使用默认十字光标")
    label.setCursor(Qt.CrossCursor) # 十字光标
else:
    print(f"成功加载图片 {icon_path}")
    new_pixmap = pixmap.scaled(30, 30)
    cursor = QCursor(new_pixmap, 15, 15)
    label.setCursor(cursor)

    print("cursor pos:",cursor.pos()) 


window.show() 


# 3. 应用程序的执行，进入到消息循环 
sys.exit(app.exec_())