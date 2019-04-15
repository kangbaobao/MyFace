from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
class WorkerOne(QThread):
 #  通过类成员对象定义信号对象
    _signal = pyqtSignal()
    def __init__(self, parent=None,time = 40,runfunc=None):
        super().__init__(parent)
        self.time = time
        # self.runfunc = runfunc
    def __del__(self):
        self.wait()
    def run(self):
        self.msleep(self.time)
        # if self.runfunc:
        #     self.runfunc()
        self._signal.emit()  # 注意这里与_signal = pyqtSignal(str)中的类型相同

class Worker(QThread):
    # sinOut = pyqtSignal()

    def __init__(self, parent=None,playFuc = None,interval=35):
        super(Worker, self).__init__(parent)
        self.working = True
        self.timer = None
        # self.num = 0
        self.playFunc = playFuc
        self.interval = interval

    def __del__(self):
        self.working = False
        self.wait()
        self.timer.stop()
    def timedone(self):
        # self.sinOut.emit()
        if self.working == False :
            self.timer.stop()
            self.quit();
            # self.wait();
        if self.playFunc :
            self.playFunc()
        # print("timedone thread : ",QThread.currentThread())

    def run(self):
        # while self.working == True:
        #     # file_str = 'File index {0}'.format(self.num)
        #     # self.num += 1
        #     # 发出信号
        #     self.sinOut.emit()
        #     # 线程休眠27毫秒
        #     self.msleep(27)
        self.timer = QTimer();
        self.timer.timeout.connect(self.timedone,Qt.DirectConnection)
        # connect(timer, SIGNAL(timeout()), this, SLOT(timedone()), Qt::DirectConnection);
        self.timer.start(self.interval);
        # print("zi thread : ",QThread.currentThread())
        self.exec();

