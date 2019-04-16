from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from MainBlockWidget import BlockModel
from CustomFaceTwoButton import CustomFaceTwoButton
def bottomLayout(leftFunc=None,rightFunc=None):
    # 创建底部layout
    h2layout = QHBoxLayout()
    h2layout.addSpacing(25)
    bottomstyle = "QPushButton {border-radius:15px;border-color:#aaaaaa;border-width:3px;border-style:solid} QPushButton:pressed{background-color:rgba(0,0,0,0.04); } "
    bottomBtn0 = QPushButton()
    bottomBtn0.setMinimumSize(100, 40)
    # bottomBtn0.setMaximumSize(125, 55)

    icon = QIcon()
    icon.addFile("./image/home-fill.png")
    bottomBtn0.setIcon(icon)
    bottomBtn0.setIconSize(QSize(30, 30))
    if leftFunc != None:
        bottomBtn0.clicked.connect(lambda x: leftFunc())
    bottomBtn0.setStyleSheet(bottomstyle);
    h2layout.addWidget(bottomBtn0)

    h2layout.addStretch(1)

    bottomBtn1 = QPushButton()
    bottomBtn1.setMinimumSize(100, 40)
    icon1 = QIcon()
    icon1.addFile("./image/fanhuiicon.png")
    bottomBtn1.setIcon(icon1)
    bottomBtn1.setIconSize(QSize(30, 30))
    if rightFunc != None:
        bottomBtn1.clicked.connect(lambda x: rightFunc())
    bottomBtn1.setStyleSheet(bottomstyle);
    h2layout.addWidget(bottomBtn1)
    h2layout.addSpacing(25)
    return h2layout

class CustomFaceTwoWidget(QWidget):
    def __init__(self,parent=None,stack=None):
        super().__init__(parent)
        self.stack = stack;
        self.initUI();
    def initUI(self):
        vlayout = QVBoxLayout()
        vlayout.addStretch(1)
        h1layout = QHBoxLayout()
        space = 40
        # h1layout.setSpacing(space)
        vlayout.addLayout(h1layout)
        # h1btn0 = CustomFaceTwoButton()
        titles = ["人脸录入","表情识别","人脸识别"];
        imgs = ["./image/erjiicon1.png","./image/erjiicon2.png","./image/erjiicon3.png"]
        bgColors = [(0,168,243),(181,235,16),(254,202,25)]
        for i in range(len(titles)):
            title = titles[i]
            img = imgs[i]
            bgColor = bgColors[i]
            model = BlockModel()
            model.img = img
            model.title = title
            model.bgColor = bgColor
            btn = CustomFaceTwoButton(model=model)
            width = (self.width() - 4.0 * space) / 3.0
            height = 80
            # btn.setGeometry(space+postion[1]*(width+space),space+postion[0]*(height+space),width,height)
            btn.setMinimumSize(width, height)
            h1layout.addWidget(btn)
            # 添加监听事件
            self.middleslot(btn, i)
        vlayout.addStretch(1)
        # 创建底部layout
        h2layout = bottomLayout(self.popnav,self.popnav)

        vlayout.addLayout(h2layout)
        vlayout.addSpacing(20)
        self.setLayout(vlayout)

    # 需要中转一下，否则每次传递的都是最后一个参数
    def middleslot(self,btn,index):
        btn.clicked.connect( lambda x: self.btnDown(x,index) )

    def btnDown(self,x,btn):
        print("btnDown: ",btn)
        if btn == 0:
            print("人脸录入的跳转")
            # 人脸录入的跳转
            from FaceThreeWiget import FaceThreeWidget
            wg = FaceThreeWidget(stack=self.stack)
            self.stack.addWidget(wg)
            self.stack.setCurrentWidget(wg)
        elif btn == 1:
            #  表情识别的跳转
            from FaceExpressionWidget import FaceExpressionWidget
            wg = FaceExpressionWidget(stack=self.stack)
            self.stack.addWidget(wg)
            self.stack.setCurrentWidget(wg)
        elif btn == 2:
            # 人脸识别的跳转
            print("人脸识别的跳转")
            from FaceRecognitionWidget import FaceRecognitionWidget
            wg = FaceRecognitionWidget(stack=self.stack)
            self.stack.addWidget(wg)
            self.stack.setCurrentWidget(wg)

    def popnav(self):
        print("popnav.....")
        print("self.stack.....: ",self.stack)
        self.stack.removeWidget(self)
        self.stack.setCurrentIndex(0)
