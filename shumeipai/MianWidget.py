from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from MainBlockWidget import MainBlockWidget,BlockModel
# from testFirstWidget import TestFirstWidget
from CustomFaceTwoWidget import CustomFaceTwoWidget


class MainWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("我是个窗口")
        self.setGeometry(0,0,1024,600)
        self.customLayout = QGridLayout();
        self.customLayout.setContentsMargins(QMargins(8,8,8,8))

        # self.customLayout.setSpacing()
        self.addCustomView();
        # self.setLayout(self.customLayout)
        # 多栈页面
        self.stack = QStackedWidget()
        mainLab = QLabel()

        # mainLab.setStyleSheet("QLabel {background-color:rgb(0,0,0); padding:1px}")
        mainLab.setLayout(self.customLayout)

        self.stack.addWidget(mainLab)
        # push2first = TestFirstWidget(stack=self.stack)
        # self.stack.addWidget(push2first)

        mainlayout = QVBoxLayout(self)
        # mainLab.setMargin(0)
        # mainlayout.setSpacing(1)
        mainlayout.setContentsMargins(QMargins(0,0,0,0))

        # mainlayout.setSpacing(0)
        mainlayout.addWidget(self.stack)
        # self.setLayout(self.stack)

    def closeEvent(self, QCloseEvent):
        from Face.KZWProcess import cPrcess
        if cPrcess:
            cPrcess.terminate()
        print("closeEvent.....")
    def addCustomView(self):
        print("addCustomView...")
        titleArr = ["人脸识别","室内环境","资讯","设备关联","留白1","留白2"]
        imgArr = ["./image/faceindex.png","./image/faceindex2.png","./image/info.png","./image/liubai.png","./image/shebei.png","./image/tianqi.png"]
        colors = [(243,137,35),(33,161,148),(241,93,93),(142,180,45),(126,97,247),(47,135,209)]
        postions = [(i,j) for i in range(3) for j in range(3)]
        for postion ,title,img,color in zip(postions,titleArr,imgArr,colors):
            model = BlockModel()
            model.title = title
            model.bgColor = color
            model.img = img
            btn = MainBlockWidget(model=model,parent=self)
            space = 10;
            width = (self.width()-4.0*space)/3.0
            height = (self.height()-3.0*space)/2.0
            # btn.setGeometry(space+postion[1]*(width+space),space+postion[0]*(height+space),width,height)
            btn.setMinimumSize(width,height)
            # 添加监听事件
            self.middleslot(btn,postion[1]+postion[0]*3)
            self.customLayout.addWidget(btn,*postion)
            self.customLayout.setSpacing(10)

    # 需要中转一下，否则每次传递的都是最后一个参数
    def middleslot(self,btn,index):
        btn.clicked.connect( lambda x: self.btnDown(x,index) )

    def btnDown(self,x,btn):
        print("btnDown: ",btn)
        if btn == 0:
            wg = CustomFaceTwoWidget(stack=self.stack)
            self.stack.addWidget(wg)
            # self.stack.setCurrentIndex(1)
            self.stack.setCurrentWidget(wg)

