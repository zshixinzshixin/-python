# 导入系统模块，用于访问命令行参数和处理程序终止
# 导入PyQt4中与窗口小部件相关的模块
import sys
from PyQt5.QtWidgets import*

# 检查是否直接运行此文件，如果是，则执行以下代码
if __name__ == '__main__':
    app = QApplication([]) 
    label = QLabel('Hello,PyQt') 
    Label_2 = QLabel('<h1>PyQt Yes!</h1>') 
    label.show()
    Label_2.show()
    sys.exit(app.exec())


# 1创建一个QApplication实例/对象,这是每个Qt应用程序必做的第一步
# 该对象的作用是接收一个列表类型的值，其实就是用来接受命令行参数的
# 由于该程序不会直接和命令行打交道所以直接传入[]即可
# 2创建一个QLabel实例,用来展示文本或图片。
# 可以直接传入图片也可以通过调用setText()
# label= QLabel()
# label.setText('Hello, PyQt!')
# 3因为控件默认都是隐藏的，所以要调用show()方法将其显示出来。
# 4通过app.exec()可以让PyQt程序运行起来.
# 而当用户正常关闭窗口时，app.exec()会返回数值0，将其传给sys.exit(),从而让Python解释器正常退出。
   