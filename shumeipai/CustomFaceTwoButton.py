from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
class CustomFaceTwoButton(QPushButton):
    def __init__(self,parent=None,model=None):
        super().__init__(parent);
        self.model = model;
        self.setStyleSheet(
            "CustomFaceTwoButton {background-color:rgb(%d,%d,%d); \
            border-radius:10px;}\
            CustomFaceTwoButton:pressed{background-color:rgba(%d,%d,%d,0.7); } "
            % (model.bgColor[0], model.bgColor[1], model.bgColor[2],
            model.bgColor[0], model.bgColor[1],
            model.bgColor[2]));
        self.label = QLabel(model.title)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-family:'msyh';font-size:20px;font-style:normal");
        self.img = QLabel()
        pix = QPixmap(model.img)
        pix = pix.scaled(40, 40, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.img.setPixmap(pix)
        layout = QHBoxLayout()
        layout.addSpacing(12)
        layout.addWidget(self.img)
        # layout.addSpacing(20)
        layout.addWidget(self.label,1)
        self.setLayout(layout)
