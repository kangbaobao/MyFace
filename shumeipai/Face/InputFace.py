import dlib         # 人脸处理的库 Dlib
import numpy as np  # 数据处理的库 Numpy
import cv2          # 图像处理的库 OpenCv
import os           # 读写文件
import shutil       # 读写文件
from .FaceUtils import cv2ImgAddText

from FilesUtils import path_photos_from_camera,path_csv_from_photos
# 进行人脸录入
class InputFace(object):
    #回调函数  writeOutput 输出打印函数  showImag 再label上 显示cv img
    def __init__(self,person_names='',writeOutput=None,showImage = None):
        self.writeOutput = writeOutput;
        self.showImage = showImage
        #外部传入的用户名参数
        self.person_names = person_names
        # Dlib 正向人脸检测器
        self.detector = dlib.get_frontal_face_detector()

        # Dlib 68 点特征预测器
        path = os.path.join('data','data_dlib','shape_predictor_68_face_landmarks.dat')
        self.predictor = dlib.shape_predictor(path)#('data/data_dlib/shape_predictor_68_face_landmarks.dat')
        print("self.predictor : ",self.predictor)
        self.cap = None
        # 人脸截图的计数器
        self.cnt_ss = 0
        self.person_cnt = 0
        self.save_flag = 0
        # self.colse = False
        self.d = None;
        self.img_rd = None;
        self.faces = 0
    #     新建文件夹
    def newFile(self):
        # 按下 'n' 新建存储人脸的文件夹
            self.person_cnt += 1
            current_face_dir = os.path.join(path_photos_from_camera, self.person_names)#path_photos_from_camera + "{0}".format(self.person_names) #+ "_" + str(self.person_cnt)
            os.makedirs(current_face_dir)
            print('\n')
            print("新建的人脸文件夹: ", current_face_dir)
            # 将人脸计数器清零
            self.cnt_ss = 0
    #     关闭摄像头
    def removeCap(self):
        # self.colse = True

        # 释放摄像头
        self.cap.release()
        # 删除建立的窗口
        # cv2.destroyAllWindows()

    def saveImage(self):
        current_face_dir = os.path.join(path_photos_from_camera, self.person_names.encode('utf-8').decode('utf-8'))#path_photos_from_camera +""+ "{0}".format(self.person_names)# + "_" + str(self.person_cnt)
        print("current_face_dir: ",current_face_dir)
        # 计算矩形框大小
        height = (self.d.bottom() - self.d.top())
        width = (self.d.right() - self.d.left())
        hh = int(height / 2)
        ww = int(width / 2)
        # 根据人脸大小生成空的图像
        im_blank = np.zeros((int(height * 2), width * 2, 3), np.uint8)
        #目前框的大小先不限制，再优化
        if len(self.faces) <= 0:
            self.writeOutput("第{0}张图片截取失败，未识别到人脸".format(self.cnt_ss))
            return
        if self.save_flag:
        # if len(self.faces) > 0:
            # 按下 's' 保存摄像头中的人脸到本地
            if os.path.isdir(current_face_dir):
                try:
                    self.cnt_ss += 1
                    for ii in range(height * 2):
                        for jj in range(width * 2):
                            im_blank[ii][jj] = self.img_rd[self.d.top() - hh + ii][self.d.left() - ww + jj]
                    filename = "img_face_" + str(self.cnt_ss) + ".jpg"
                    path = os.path.join( current_face_dir, filename)
                    print("save_image  cv2.imwrite :",path)
                    # path =path.replace('\\','/')
                    # cv2.imwrite(path, im_blank)
                    print(" cv2.imencode('.jpg', im_blank) :", cv2.imencode('.jpg', im_blank))
                    cv2.imencode('.jpg', im_blank)[1].tofile(path)
                    print("写入本地：", str(path) + "/img_face_" + str(self.cnt_ss) + ".jpg")
                    self.writeOutput("第{0}张人脸图保存成功".format(self.cnt_ss))
                except Exception as e:
                    print("e : ",e)
                    self.writeOutput("第{0}张图片截取失败，请继续截取".format(self.cnt_ss))
                    self.cnt_ss -= 1


            else:
                self.writeOutput("请先新建文件夹再保存")
                print("请在按 'S' 之前先按 'N' 来建文件夹 / Please press 'N' before 'S'")
        else:
            self.writeOutput("保存截图失败，请调整人脸位置，请在识别框为白色时截图")
            print("保存截图失败为识别到人脸未识别到人脸");
    def Handler(self):
        pass
    # qTimer 定时器调用他
    def whileShow(self):
        if self.cap.isOpened():
            # 480 height * 640 width
            flag, img_rd = self.cap.read()
            if img_rd is None:
                return
            self.img_rd = img_rd
            # cv2.waitKey(1000)
            # print("while..........")
            img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)

            # 人脸数 faces
            faces = self.detector(img_gray, 0)
            self.faces = faces
            # 待会要写的字体
            font = cv2.FONT_HERSHEY_COMPLEX

            # 检测到人脸
            if len(faces) != 0:
                # 矩形框
                for k, d in enumerate(faces):
                    self.d = d;
                    # 计算矩形大小
                    # (x,y), (宽度width, 高度height)
                    pos_start = tuple([d.left(), d.top()])
                    pos_end = tuple([d.right(), d.bottom()])

                    # 计算矩形框大小
                    height = (d.bottom() - d.top())
                    width = (d.right() - d.left())

                    hh = int(height / 2)
                    ww = int(width / 2)
                    # print("height: {} width: {}".format(height,width))
                    # print("hh: {} ww: {}".format(hh,ww))

                    # 设置颜色 / The color of rectangle of faces detected
                    color_rectangle = (255, 255, 255)
                    if (d.right() + ww) > 640 or (d.bottom() + hh > 480) or (d.left() - ww < 0) or (d.top() - hh < 0):
                        cv2.putText(img_rd, "OUT OF RANGE", (20, 300), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                        color_rectangle = (0, 0, 255)
                        self.save_flag = 0
                    else:
                        color_rectangle = (255, 255, 255)
                        self.save_flag = 1
                    cv2.rectangle(img_rd,
                                  tuple([d.left() - ww, d.top() - hh]),
                                  tuple([d.right() + ww, d.bottom() + hh]),
                                  color_rectangle, 2)

            # 显示人脸数
            cv2.putText(img_rd, "Faces: " + str(len(faces)), (20, 100), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
            # self.img_rd = cv2ImgAddText(img_rd,'人脸数：'+str(len(faces)),20,100,  (0, 255, 255), 14)

            # # 添加说明
            # cv2.putText(img_rd, "Face Register", (20, 40), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
            # cv2.putText(img_rd, "N: New face folder", (20, 350), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
            # cv2.putText(img_rd, "S: Save current face", (20, 400), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
            # cv2.putText(img_rd, "Q: Quit", (20, 450), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)

            # # 按下 'q' 键退出
            # if self.colse:
            #     break
            # 窗口显示
            # cv2.namedWindow("camera", 0) # 如果需要摄像头窗口大小可调
            # cv2.imshow("camera", img_rd)
            # self.showImage(img_rd);
    def openCap(self):
        # OpenCv 调用摄像头
        self.cap = cv2.VideoCapture(0)
        # 设置视频参数
        # self.cap.set(3, 480)
         # 编码格式
        self.cap.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
         # 设置视频参数
        self.cap.set(3, 480)
         # 设置视频参数高
        self.cap.set(4, 640)
        # # 视屏的宽
        # self.cap.set(3, 1920)
        # # 视频每一帧的高
        # self.cap.set(4,1080)

