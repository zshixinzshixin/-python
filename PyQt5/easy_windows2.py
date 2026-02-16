import sys
from PyQt5.QtWidgets import *
import os

print("Current Working Directory:", os.getcwd())
if __name__ == '__main__':
    app = QApplication([])
    label = QLabel()
    with open('test.html', 'r', encoding='UTF-8') as f:
        label.setText(f.read())
    label.show()
    sys.exit(app.exec())

# d:\\Pythonsss\\PyQt5\\test.html