# 代码功能：演示QObject的继承关系
from PyQt5.Qt import *

# print(QObject.__subclasses__()) # QObject的所有直接子类
# print(QWidget.__subclasses__()) # QWidget的所有直接子类
# print(QAbstractButton.__subclasses__()) # QAbstractButton的所有直接子类

def getSubClasses(cls):
    # 打印当前类的所有子类
    for sub_class in cls.__subclasses__():
        print(sub_class)
        if len(cls.__subclasses__()) > 0:
            getSubClasses(sub_class)

# print("QObject的所有子类：")
# getSubClasses(QObject)
