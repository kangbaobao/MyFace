from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# from PyQt5 import Qt
from  PyQt5.QtCore import Qt
class BlockModel():
    def __init__(self):
        # #背景颜色
        self.bgColor = (0,0,0)
        #设置标题
        self.title = "";
        #设置图标
        self.img = None;
class MainBlockWidget(QPushButton):
    def __init__(self,parent=None,model=None):
        super().__init__(parent)
        QFontDatabase.addApplicationFont("./font/msyh.ttc")

        self.model = model;
        self.setStyleSheet("MainBlockWidget {background-color:rgb(%d,%d,%d);border-radius:10px;} MainBlockWidget:pressed{background-color:rgba(%d,%d,%d,0.7); } " % (model.bgColor[0],model.bgColor[1],model.bgColor[2],model.bgColor[0],model.bgColor[1],model.bgColor[2]));
        self.label = QLabel(model.title)
        self.label.setStyleSheet("font-family:'msyh';font-size:20px;font-style:normal");
        self.img = QLabel()
        pix = QPixmap(model.img)
        pix = pix.scaled(70,70,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        self.img.setPixmap(pix)
        layout = QVBoxLayout();
        layout.addSpacing(10)
        layout.addWidget(self.label)
        layout.addStretch(1)
        hl = QHBoxLayout()
        hl.addStretch(1)
        hl.addWidget(self.img)
        hl.addStretch(1)
        # layout.addWidget(self.img)
        layout.addItem(hl)
        layout.addSpacing(10)
        layout.addStretch(1)
        self.setLayout(layout)




