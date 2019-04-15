import sys
from PyQt5.QtWidgets import*
from PyQt5.QtGui import *
from MianWidget import MainWidget
from PyQt5.QtCore import Qt
from PyQt5.QtCore import *

from Db import *
from FilesUtils import pre_work_mkdir,path_csv_from_photos,path_photos_from_camera
import os
from Face.KZWProcess import runProcess
# 测试
from MainBlockWidget import MainBlockWidget,BlockModel
if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = QDesktopWidget().screenGeometry()
    print("screen width:",screen.width())
    print("screen height:",screen.height())
    # 创建保存用户数据的文件夹
    pre_work_mkdir(path_photos_from_camera)
    pre_work_mkdir(path_csv_from_photos)
    # # 测试
    # csv_rd = os.listdir(path_photos_from_camera)
    # csv_rd.sort()
    # print("##### 得到的特征均值 / The generated average values of features stored in: #####")
    # for i in range(len(csv_rd)):
    #     print(csv_rd[i])
    w = MainWidget()
    w.show()
    print("zhu thread : ", QThread.currentThread())
    #开启多进程
    runProcess()
    # w.close().connect(customProcess.terminate())

    sys.exit(app.exec_())
