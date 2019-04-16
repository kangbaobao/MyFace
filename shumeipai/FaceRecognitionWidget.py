'''人脸识别界面'''
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from CustomFaceTwoWidget import bottomLayout
from Face.FaceRecongnition import FaceRecongnition
from MyThread import Worker,WorkerOne
import multiprocessing
class FaceRecognitionWidget(QWidget):
    def __init__(self,parent=None,stack=None):
        super().__init__(parent)
        self.stack = stack
        self.supdatestr= ''
        self.initUI()
        self.updateScroll("数据正在初始化，请稍后...")
        self.initThread = WorkerOne(parent=self, time=1)
        # 连接信号
        self.initThread._signal.connect(self.asyncInit)  # 进程连接回传到GUI的事件
        # 开始线程
        self.initThread.start()
        # self.asyncInit()
        print("process : ",multiprocessing.current_process().pid)
        # #多进程编程
        # self.mprocess = multiprocessing.Process(name="dataHandler",target=self.playProcess,args=(self,))
        # self.mprocess.daemon = True;
        # self.mprocess.start()


    # def playProcess(self):
    #     print("process : ",multiprocessing.current_process().pid)
    #     # self.timer = QTimer();
    #     # self.timer.timeout.connect(self.timedoneProcess)
    #     # self.timer.start(35);
    #
    # def timedoneProcess(self):
    #     print("timedoneProcess : ",multiprocessing.current_process().pid)

    def asyncInit(self):
        self.mthread = Worker(parent=self, playFuc=self.play)
        self.mthread2 = Worker(parent=self, playFuc=self.play2,interval=2500)
        # from Face.InputFace import InputFace
        # self.recFace = InputFace(self.updateScroll,self.showImage)

        self.recFace = FaceRecongnition(self.updateScroll,self.rightTopStr)
        self.recFace.openCap()
        self.mthread.start()
        self.mthread2.start()
    def play2(self):
        # 读取数据
        self.recFace.Handler()
        QCoreApplication.processEvents()

    def play(self):
        # 读取数据
        self.recFace.whileShow()
        self.showImage(self.recFace.img_rd)
        QCoreApplication.processEvents()

    # 实时刷新展示人脸数据
    def showImage(self, img):
        # if img :
        if img is None:
            return
        height, width, channel = img.shape
        bytesPerline = 3 * width;
        qImg = QImage(img.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        img = QPixmap.fromImage(qImg)
        img.scaled(self.capLab.size(), Qt.KeepAspectRatioByExpanding)
        self.capLab.setPixmap(img)


    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        # 摄像头label
        self.capLab = QLabel("")
        self.capLab.setStyleSheet("border-color:#aaaaaa;border-width:1px;border-style:solid;")
        layout.addWidget(self.capLab,3)

        rightLayout = QVBoxLayout()
        layout.addLayout(rightLayout,1)

        self.infolab = QLabel("\t人脸信息\n\n\n当前人脸数：--\n当前人脸名：--")
        self.infolab.setStyleSheet("border-color:#aaaaaa;border-width:1px;border-style:solid;font-size:20px;")
        self.infolab.setAlignment(Qt.AlignLeft | Qt.AlignTop);  # 居中对齐
        self.infolab.setMargin(10)
        self.infolab.setMaximumSize(400, 800)
        self.infolab.setScaledContents(True)  # 让图片自适应label大小

        rightLayout.addWidget(self.infolab,1)
        # 输出日志的label
        self.outLab = QLabel("提示日志：\n ")
        self.outLab.setAlignment(Qt.AlignTop)
        # self.outLab.setStyleSheet("border-color:#aaaaaa;border-width:1px;border-style:solid;padding:8px")
        self.outLab.setWordWrap(True)
        self.outLab.setMargin(5)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.outLab);
        self.scrollArea.setAlignment(Qt.AlignLeft | Qt.AlignTop);  # 居中对齐
        self.scrollArea.widgetResizable = False
        rightLayout.addWidget(self.scrollArea,1)
        hlayout2 = bottomLayout(self.backhome,self.popnav)
        rightLayout.addLayout(hlayout2)
        # self.capLab.setMaximumSize(self.capLab.width(), self.capLab.height())
        self.capLab.setScaledContents(True)  # 让图片自适应label大小

    # 更新日志
    def rightTopStr(self,count,name):
        str = "\t人脸信息\n\n\n当前人脸数：{0}\n当前人脸名：{1}".format(count,name)
        self.infolab.setText(str)
    # def asyncUpateScroll(self, newStr=None):
    #     self.supdatestr = newStr
    #     oneThread = WorkerOne(parent=self, time=0)
    #     # 连接信号
    #     oneThread._signal.connect(self.asyncInit)  # 进程连接回传到GUI的事件
    #     # 开始线程
    #     oneThread.start()
    # def asyncScroll(self):
    #     self.updateScroll(self.supdatestr)
    def updateScroll(self, newStr=None):
        oldstr = self.outLab.text()
        self.scrollArea.takeWidget();
        self.outLab = None
        self.outLab = QLabel()
        self.outLab.setWordWrap(True)
        self.outLab.setMargin(5)
        self.outLab.setMaximumWidth(self.scrollArea.width() - 30)
        str = oldstr + "\n" + newStr;
        self.outLab.setText(str)
        self.scrollArea.setWidget(self.outLab)
        # 设置 scrollArea左右禁止滚动
        # 滚动到底
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum());  # 直接滚到底
        # 滚动到左边
        self.scrollArea.horizontalScrollBar().setValue(self.scrollArea.horizontalScrollBar().minimum())
    # 返回上一级
    def backhome(self):
        print("backhome....")
        # if self.timer:
        #     self.timer.stop()
        if self.mthread:
            self.mthread.working = False
        if self.mthread2:
            self.mthread2.working = False
        if self.recFace:
            self.recFace.removeCap()
        self.stack.removeWidget(self)
        self.stack.setCurrentIndex(0)

    # 返回到主页
    def popnav(self):
        print("popnav....")
        # if self.timer:
        #     self.timer.stop()
        if self.mthread:
            self.mthread.working = False
        if self.mthread2:
            self.mthread2.working = False
        if self.recFace:
            self.recFace.removeCap()
        self.stack.removeWidget(self)







