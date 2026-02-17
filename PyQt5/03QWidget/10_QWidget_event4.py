# 代码功能：窗口移动（只有左键按下才移动窗口）
from PyQt5.Qt import * 
import sys


class Window(QWidget): 
    def __init__(self): 
        super().__init__() 
        self.setWindowTitle("事件消息案例") 
        self.resize(500, 500) 
        self.setup_ui() 

    def setup_ui(self): 
        pass 

    def mousePressEvent(self, evt): 
        if evt.button() == Qt.LeftButton: # 只有左键按下才移动窗口
            self.move_flag = True
            print("mousePressEvent：鼠标按下了") 
            # 记录鼠标按下时的全局坐标
            self.mousePress_x = evt.globalX() 
            self.mousePress_y = evt.globalY() 
            # 记录窗口当前的位置
            self.windowOrigin_x = self.x() 
            self.windowOrigin_y = self.y() 
        
    def mouseReleaseEvent(self, evt): 
        print("mouseReleaseEvent：鼠标释放了") 
        self.move_flag = False
    
    def mouseMoveEvent(self, evt): 
        if self.move_flag:
            print("mouseMoveEvent：鼠标移动了") 
            # 计算移动距离
            move_x = evt.globalX() - self.mousePress_x 
            move_y = evt.globalY() - self.mousePress_y 
            # 计算新位置并移动窗口
            new_x = self.windowOrigin_x + move_x 
            new_y = self.windowOrigin_y + move_y 
            self.move(new_x, new_y) 



if __name__ == '__main__': 
    app = QApplication(sys.argv) 
    window = Window() 
    window.show() 
    sys.exit(app.exec_())