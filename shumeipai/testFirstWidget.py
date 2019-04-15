from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
class TestFirstWidget(QWidget):
    def __init__(self,parent=None,stack=None):
        super().__init__(parent)
        print("TestFirstWidget.....")
        self.stack = stack
        self.setStyleSheet("TestFirstWidget { background-color:rgb(255,0,0); }")
        # self.setMinimumSize(parent.width(),parent.height())
        self.btn = QPushButton("返回",self)
        self.btn.clicked.connect( lambda x: self.popnav(x,self.btn) )

    def popnav(self,x,btn):
        print("popnav.....")
        print("self.stack.....: ",self.stack)
        self.stack.removeWidget(self)
        self.stack.setCurrentIndex(0)


