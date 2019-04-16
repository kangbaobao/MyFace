# 表情识别 widget
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QLabel
from PyQt5.QtCore import QCoreApplication,Qt
from PyQt5.QtGui import *
# from PyQt5 import Qt
from CustomFaceTwoWidget import bottomLayout
from MyThread import Worker
from Face.Face_Expression import face_emotion
class FaceExpressionWidget(QWidget):
    def __init__(self,parent=None,stack=None):
        super().__init__(parent)
        self.stack = stack
        self.initUI()
        self.mthread = Worker(parent=self, playFuc=self.play)
        self.recFace = face_emotion()
        # 打开摄像头
        self.recFace.openCap()
        #开启线程
        self.mthread.start()

    def play(self):
        # 读取数据
        self.recFace.whileShow()
        self.showImage(self.recFace.img_rd)
        QCoreApplication.processEvents()

    # 实时刷新展示人脸数据
    def showImage(self, img):
        if img is None:
            return
        height, width, channel = img.shape
        bytesPerline = 3*width;
        qImg = QImage(img.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        img = QPixmap.fromImage(qImg)
        img.scaled(self.capLab.size(), Qt.KeepAspectRatioByExpanding)#Qt.KeepAspectRatioByExpanding)
        self.capLab.setPixmap(img)
    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        # 摄像头label
        self.capLab = QLabel("")
        self.capLab.setStyleSheet("border-color:#aaaaaa;border-width:1px;border-style:solid;")
        layout.addWidget(self.capLab, 1)
        hlayout2 = bottomLayout(self.backhome, self.popnav)
        layout.addLayout(hlayout2)
        self.capLab.setScaledContents(True)  # 让图片自适应label大小
        self.setMaximumSize(self.stack.width(),self.stack.height())

    #  返回到主页
    def backhome(self):
        print("backhome....")
        if self.mthread:
            self.mthread.working = False
        # if self.recFace:
        #     self.recFace.removeCap()
        self.stack.removeWidget(self)
        self.stack.setCurrentIndex(0)

    # 返回上一级
    def popnav(self):
        print("popnav....")
        if self.mthread:
            self.mthread.working = False
        # if self.recFace:
        #     self.recFace.removeCap()
        self.stack.removeWidget(self)
