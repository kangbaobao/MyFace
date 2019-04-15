from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from MainBlockWidget import BlockModel
from CustomFaceTwoButton import CustomFaceTwoButton
from Db import User
import Db
import os
from sqlalchemy.exc import IntegrityError
from FilesUtils import pre_work_mkdir, path_csv_from_photos, path_photos_from_camera
from Face.InputFace import InputFace
# from Face.FaceToCSV import FaceToCSV
from MyThread import Worker
import cv2
class FaceThreeWidget(QWidget):
    def __init__(self,parent=None,stack=None):
        super().__init__(parent)
        print("-------------------------")
        self.stack = stack
        self.inputFace = None
        self.mthread = Worker(parent=self,playFuc=self.play)
        self.name = ''
        self.initUI()
    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        hlayout0 = QHBoxLayout()
        hlayout1 = QHBoxLayout()
        from CustomFaceTwoWidget import bottomLayout
        hlayout2 = bottomLayout(self.backhome,self.popnav)
        space = 12
        layout.addSpacing(space)
        layout.addLayout(hlayout0,1)
        layout.addSpacing(space)
        layout.addLayout(hlayout1)
        layout.addSpacing(space)
        layout.addLayout(hlayout2)
        layout.addSpacing(space)
        #摄像头视图 label
        self.capLab = QLabel("我是摄像头")
        self.capLab.setStyleSheet("border-color:#aaaaaa;border-width:1px;border-style:solid;")
        # 输出日志块视图

        # 输出日志的label
        self.outLab = QLabel("提示日志：\n 请在底部的输入框你的姓名用已保存你的信息，输入结束点击\"创建人脸信息\"按钮完成")
        self.outLab.setAlignment(Qt.AlignTop)
        # self.outLab.setStyleSheet("border-color:#aaaaaa;border-width:1px;border-style:solid;padding:8px")
        self.outLab.setWordWrap(True)
        self.outLab.setMargin(5)
        # contentWidget = QWidget()
        # contenLayout = QHBoxLayout()
        # contenLayout.addWidget(self.outLab)
        # contentWidget.setLayout(contenLayout)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.outLab);
        self.scrollArea.setAlignment(Qt.AlignLeft|Qt.AlignTop);  # 居中对齐
        self.scrollArea.widgetResizable = False
        hlayout0.setSpacing(space)
        hlayout0.addWidget(self.capLab,3)
        hlayout0.addWidget(self.scrollArea,2)

        # 新建输入框
        self.input = QLineEdit()
        self.input.setPlaceholderText("请输入你的姓名")
        self.input.setMinimumSize(150, 40)
        self.input.setMaximumSize(250, 40)
        hlayout1.addWidget(self.input)

        # 新建文件夹 截图  运算
        titles = ["创建人脸信息", "截图", "运算"];
        imgs = ["./image/folder-open.png", "./image/camera.png", "./image/calculator.png"]
        bgColors = [(196, 255, 14), (63, 72, 204), (254, 202, 25)]
        for i in range(len(titles)):
            title = titles[i]
            img = imgs[i]
            bgColor = bgColors[i]
            model = BlockModel()
            model.img = img
            model.title = title
            model.bgColor = bgColor
            btn = CustomFaceTwoButton(model=model)
            # width = 150
            # height = 50
            btn.setMinimumSize(150, 55)
            btn.setMaximumSize(200, 55)
            hlayout1.addWidget(btn)
            # 添加监听事件
            self.middleslot(btn, i)
        self.capLab.setMaximumSize(self.capLab.width(),self.capLab.height())
        self.capLab.setScaledContents (True)  # 让图片自适应label大小

    # 需要中转一下，否则每次传递的都是最后一个参数
    def middleslot(self, btn, index):
        btn.clicked.connect(lambda x: self.btnDown(index))

    # 实时刷新展示人脸数据
    def showImage(self,img):
        # print("img.type() :",img.type)
        # cv2.CV_8UC4

        height,width,channel = img.shape
        bytesPerline = 3*width;
        qImg = QImage(img.data,width,height,bytesPerline,QImage.Format_RGB888).rgbSwapped()
        img = QPixmap.fromImage(qImg)
        img.scaled(self.capLab.size(), Qt.KeepAspectRatioByExpanding)
        self.capLab.setPixmap(img)
        # print("showImage thread : ",QThread.currentThread())


    def btnDown(self,index):
        print("index: ",index)
        if index == 0:
            # 新建文件加 名字现在是唯一表示，不可重复
            namestr = self.input.text();
            self.name = namestr
            namestr = namestr.strip()
            if namestr == '' or namestr is None:
                self.input.setText("")
                self.updateScroll("输入的名字不能为空")
                return ;
            self.newPresonData(namestr);
            pass
        elif index == 1:
            if self.inputFace:
                self.inputFace.saveImage()
        elif index == 2 :
            self.updateScroll("数据录入中，请耐心等候。。。。")
            if self.name == '' or self.name is None:
                self.updateScroll("请先创建文件夹")
            from Face.FaceToCSV import FaceToCSV
            tocvs = FaceToCSV(self.name,self.updateScroll)
            tocvs.WriteCSV()

    #    数据库插入我的信息 并新建文件同名 报错我的截图
    def newPresonData(self,str=None):
        # 数据库操作
        if str is None or str == '':
            self.updateScroll(" 插入的数据不能为空")
            return
        try:
            # 新建 用户的数据
            new_user = User(name=str)
            Db.session.add(new_user)
            Db.session.commit()

        except IntegrityError as e:
            print("e: ",e)
            self.updateScroll("用户名已在数据库中存在，不可再次新建这个用户名的数据，请更换输入的用户名")
            Db.session.rollback()
        else:
            #  新建用户文件夹
            userdir = os.path.join(path_photos_from_camera, str)
            print("newPresonData usedir: ",userdir)
            pre_work_mkdir(userdir)
            self.updateScroll("用户名已保存，开启摄像头后请用户点击十次截图，用以记录用户脸部特征参数")
            # 人脸录入类
            self.inputFace = InputFace(str,self.updateScroll, self.showImage)
            # 打开摄像头
            self.inputFace.openCap()
            # self.timer.start(40)
            self.mthread.start()


    def play(self):
        #读取数据
        self.inputFace.whileShow()
        self.showImage(self.inputFace.img_rd)
        QCoreApplication.processEvents()
        # print("play thread : ",QThread.currentThread())


    # 更新日志
    def updateScroll(self, newStr=None):
        oldstr = self.outLab.text()
        # print("scrollArea: ",self.scrollArea.width())
        self.scrollArea.takeWidget();
        self.outLab = None
        self.outLab = QLabel()
        # self.outLab.setAlignment(Qt.AlignTop)
        self.outLab.setWordWrap(True)
        self.outLab.setMargin(5)
        # self.outLab.setStyleSheet("border-color:#aaaaaa;border-width:1px;border-style:solid;padding:8px")
        self.outLab.setMaximumWidth(self.scrollArea.width()-30)
        str = oldstr+"\n"+newStr;
        self.outLab.setText(str)
        self.scrollArea.setWidget(self.outLab)
        # 设置 scrollArea左右禁止滚动
        # 滚动到底
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum());  # 直接滚到底
        # 滚动到左边
        self.scrollArea.horizontalScrollBar().setValue(self.scrollArea.horizontalScrollBar().minimum())

    #返回上一级
    def backhome(self):
        print("backhome....")
        # if self.timer:
        #     self.timer.stop()
        self.mthread.working = False
        if self.inputFace:
            self.inputFace.removeCap()
        self.stack.removeWidget(self)
        self.stack.setCurrentIndex(0)
    # 返回到主页
    def popnav(self):
        print("popnav....")
        # if self.timer:
        #     self.timer.stop()
        self.mthread.working = False
        if self.inputFace:
            self.inputFace.removeCap()
        self.stack.removeWidget(self)
