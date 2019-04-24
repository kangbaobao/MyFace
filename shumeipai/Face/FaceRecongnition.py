# 摄像头实时人脸识别
import dlib          # 人脸处理的库 Dlib
import numpy as np   # 数据处理的库 numpy
import cv2           # 图像处理的库 OpenCv
import pandas as pd  # 数据处理的库 Pandas
import os
from FilesUtils import path_photos_from_camera,path_csv_from_photos
import json
import math
from PyQt5.QtCore import QThread
from .FaceUtils import cv2ImgAddText
import copy
DATANOFACE = "未录入"
DATAINITFACE = "未知"
from .KZWProcess import qInput,qOutput
from queue import Empty


# 计算两个128D向量间的欧式距离
def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    # print("e_distance: ", dist)
    if dist > 0.4:
        return "diff"
    else:
        return "same"
# 缓存识别过的人脸数据 减少for循环次数
class FaceData(object):
    def __init__(self,name='',data=None):
        self.name = name
        self.data = data
class FaceRecongnition(object):
    def __init__(self,writeOutput=None,topInfoFunc=None):
        self.writeOutput = writeOutput;
        self.topInfoFunc = topInfoFunc
        self.img_rd = None;
        self.cap = None
        path = os.path.join('data','data_dlib','dlib_face_recognition_resnet_model_v1.dat')
        # 人脸识别模型，提取128D的特征矢量
        self.facerec = dlib.face_recognition_model_v1(path)

        self.writeOutput("正在进行人脸识别")
        # 存放是别的人名
        self.knownlist = []
        #存放识别到的人的位置
        self.postion = []
        # 识别过的人脸缓存在这里
        self.recList = []
        #缓存人脸数
        self.facesLen = 0

 # 处理存放所有人脸特征的 csv
        path_features_known_csv = os.path.join('data','features_all.csv')#"data/features_all.csv"
        self.csv_rd = pd.read_csv(path_features_known_csv, header=None)
        # 存储的特征人脸个数
        # print(csv_rd.shape[0])
        # 用来存放所有录入人脸特征的数组
        self.features_known_arr = []
        # 读取已知人脸数据
        # known faces
        for i in range(self.csv_rd.shape[0]):
            features_someone_arr = []
            for j in range(0, len(self.csv_rd.ix[i, :])):
                features_someone_arr.append(self.csv_rd.ix[i, :][j])
                self.features_known_arr.append(features_someone_arr)
        print("Faces in Database：", self.features_known_arr)
        self.load_list = []
        jsonpath = os.path.join('data','user.json')
        with open(jsonpath, 'r') as load_f:
            self.load_list = json.load(load_f)


        # Dlib 检测器和预测器
        self.detector = dlib.get_frontal_face_detector()
        spath = os.path.join('data','data_dlib','shape_predictor_68_face_landmarks.dat')
        self.predictor = dlib.shape_predictor(spath)
    # 打开摄像头
    def openCap(self):
        # 创建 cv2 摄像头对象
        self.cap = cv2.VideoCapture(0)

        # cap.set(propId, value)
        # 设置视频参数，propId 设置的视频参数，value 设置的参数值
        # self.cap.set(3, 480)
         # 编码格式
        self.cap.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        # # 视屏的宽
        # self.cap.set(3, 1920)
        # # 视频每一帧的高
        # self.cap.set(4,1080)
        self.cap.set(3, 480)
         # 设置视频参数高
        self.cap.set(4, 640)

        # 返回一张图像多张人脸的 128D 特征
    def get_128d_features(self,img_gray):
        faces = self.detector(img_gray, 1)
        if len(faces) != 0:
            face_des = []
            for i in range(len(faces)):
                shape = self.predictor(img_gray, faces[i])
                face_des.append(self.facerec.compute_face_descriptor(img_gray, shape))
        else:
            face_des = []
        return face_des


 #
    def whileShow(self):
        # print("whileShow :",QThread.currentThread());
        if self.cap.isOpened():
            flag, img_rd = self.cap.read()
            if img_rd is None:
                return
            self.img_rd = img_rd
            # 取灰度
            img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)
            # 人脸数 faces
            faces = self.detector(img_gray, 0)
            # 检测到人脸
            if len(faces) != 0:
                # 遍历捕获到的图像中所有的人脸
                for k in range(len(faces)):
                    # 让人名跟随在矩形框的下方
                    d = faces[k]
                    cv2.rectangle(img_rd, tuple([d.left(), d.top()]), tuple([d.right(), d.bottom()]),
                                      (0, 255, 255), 2)
                    if len(self.knownlist)>k:

                        if self.knownlist[k] == DATAINITFACE or self.knownlist[k] == DATANOFACE or len(self.knownlist)<=1:
                            self.img_rd = cv2ImgAddText(img_rd, self.knownlist[k],  d.left(),
                                                     d.bottom()+5, (0, 255, 255), 14)
                        else:
                            self.img_rd = cv2ImgAddText(img_rd, self.knownlist[k], self.postion[k][0],
                                                     self.postion[k][1], (0, 255, 255), 14)
                self.facesLen = len(faces)
            else:
                #人脸数为0
                self.knownlist.clear()

                # if len(self.knownlist) == len(faces):
                    #     self.img_rd = cv2ImgAddText(img_rd, self.knownlist[k], d.left(), faces[k].bottom()+5,  (0, 255, 255), 14)

#     def Handler(self):
#         if self.img_rd is None:
#             return
#         if  self.img_rd.data:
#             # flag, img_rd = self.cap.read()
#             img_rd =copy.deepcopy(self.img_rd) #self.img_rd
#             # 取灰度
#             img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)
#             # 人脸数 faces
#             faces = self.detector(img_gray, 0)
#             # 存储当前摄像头中捕获到的所有人脸的坐标/名字
#             # pos_namelist = []
#             name_namelist = []
#             # if len(faces) == self.facesLen: return
#             # 检测到人脸
#             if len(faces) > 0:
#                 # 获取当前捕获到的图像的所有人脸的特征，存储到 features_cap_arr
#                 features_cap_arr = []
#
#                 # 遍历捕获到的图像中所有的人脸
#                 for k in range(len(faces)):
#                     # 让人名跟随在矩形框的下方
#                     # name_namelist.append(DATAINITFACE)
#                     shape = self.predictor(img_rd, faces[k])
#                     features_cap_arr.append(self.facerec.compute_face_descriptor(img_rd, shape))
#
# # 进程
#                     #获取在进程中计算人脸是谁
#                     qInput.put(features_cap_arr[k])
#                     try:
#                         ouputNameDic = qOutput.get(block=True, timeout=3)
#                         # print("k : ",k)
#
#                         # name_namelist[k] = ouputNameDic["name"]
#                         if ouputNameDic["name"] in name_namelist:
#                             pass
#                         else:
#                             name_namelist.append(ouputNameDic["name"])
#                         print("ouputNameDic: ",ouputNameDic)
#                         #防止重复插入
#                         for recindex in range(len(self.recList)):
#                             if self.recList[recindex].name == ouputNameDic["name"]:
#                                 self.recList.pop(recindex)
#                                 break
#                                 #hasName = True
#                         face = FaceData(name=  ouputNameDic["name"],data=ouputNameDic["data"])
#                         self.recList.append(face)
#
#                         self.topInfoFunc(len(faces),",".join(name_namelist))
#                         print("output: ",name_namelist)
#                     except Empty as e:
#                             pass
# 进程



    # qTimer 定时器调用他
    def Handler(self):
        # print("Handler.............")
        if self.img_rd is None:
            return
        if  self.img_rd.data:
            # flag, img_rd = self.cap.read()
            img_rd =copy.deepcopy(self.img_rd) #self.img_rd
            # 取灰度
            img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)
            # 人脸数 faces
            faces = self.detector(img_gray, 0)
            # 存储当前摄像头中捕获到的所有人脸的坐标/名字
            pos_namelist = []
            name_namelist = []
            # 检测到人脸
            if len(faces) > 0:
                # 获取当前捕获到的图像的所有人脸的特征，存储到 features_cap_arr
                features_cap_arr = []

                # 遍历捕获到的图像中所有的人脸
                for k in range(len(faces)):
                    # 让人名跟随在矩形框的下方
                    name_namelist.append(DATAINITFACE)
                    pos_namelist.append((0,0))

                    shape = self.predictor(img_rd, faces[k])
                    features_cap_arr.append(self.facerec.compute_face_descriptor(img_rd, shape))

                    # if len(faces) == self.facesLen and len(self.knownlist)>= len(faces) :
                    #     # print("recList : len(faces) ",len(faces))
                    #     # print("recList : self.facesLen ",self.facesLen)
                    #     for i in range(len(self.recList)):
                    #         compare = return_euclidean_distance(features_cap_arr[k], self.recList[i].data)
                    #         if compare == "same":  # 找到了相似脸
                    #             # index = math.floor(i/128.0)
                    #             name_namelist[k] = self.recList[i].name
                    #             self.topInfoFunc(len(faces),",".join(name_namelist))
                    #         # 如果 当前人是未知的话需要查询数据库
                    #         if name_namelist[k] == DATAINITFACE:
                    #             self.allForCSV(name_namelist=name_namelist,k=k,features_cap_arr=features_cap_arr,faces=faces)
                    #         # else:
                    # else:
                    #     self.allForCSV(name_namelist=name_namelist,k=k,features_cap_arr=features_cap_arr,faces=faces)
                    # self.allForCSV(name_namelist=name_namelist,k=k,features_cap_arr=features_cap_arr,faces=faces,pos_namelist=pos_namelist)

                    # 对于某张人脸，遍历所有存储的人脸特征
                    for i in range(len(self.features_known_arr)):
                        # print("with person_", str(i + 1), "the ", end='')
                        # 将某张人脸与存储的所有人脸数据进行比对
                        compare = return_euclidean_distance(features_cap_arr[k], self.features_known_arr[i])
                            # print("i : ",i)
                        if compare == "same":  # 找到了相似脸
                            #总共一个人有128个特征点 所以i/128向下取整就是 这个的的index
                            index = math.floor(i/128.0)
                            if len(name_namelist)>index:
                                name_namelist[k] = self.load_list[index]
                                pos_namelist[k] = (faces[k].left(),faces[k].bottom() + 5)
                        # else:
                        #     pos_namelist[k] = (faces[k].left(),faces[k].bottom() + 5)


                            #防止重复插入
                            hasName = False
                            # for recindex in range(len(self.recList)):
                            #     if self.recList[recindex].name == name_namelist[k]:
                            #         hasName = True
                            # if hasName is False :
                            for recindex in range(len(self.recList)):
                                if len(name_namelist)>k:
                                    if self.recList[recindex].name == name_namelist[k]:
                                        self.recList.pop(recindex)
                                        break
                            if len(name_namelist)>k:
                                face = FaceData(name= name_namelist[k],data=self.features_known_arr[i])
                                self.recList.append(face)
                            # print("features_known_arr same...")

                            # 姓名列表
                            self.knownlist = name_namelist
                            self.postion = pos_namelist
                        self.topInfoFunc(len(faces),",".join(name_namelist))


                # #记录的人脸数
                # self.facesLen = len(faces)
            else:
                # pass
                 #self.facesLen = 0
                # 没有检测到人脸
                self.topInfoFunc(len(faces), "")
            # 缓存人脸数 人脸数变换 则查询所有数据库所有数据
    def allForCSV(self,name_namelist,k,features_cap_arr,faces,pos_namelist):
        for i in range(len(self.features_known_arr)):
            # print("with person_", str(i + 1), "the ", end='')
            # 将某张人脸与存储的所有人脸数据进行比对
            compare = return_euclidean_distance(features_cap_arr[k], self.features_known_arr[i])
                # print("i : ",i)
            if compare == "same":  # 找到了相似脸
                #总共一个人有128个特征点 所以i/128向下取整就是 这个的的index
                index = math.floor(i/128.0)
                print("len load_list : ",len(self.load_list),index)
                name_namelist[k] = self.load_list[index]
                pos_namelist[k] = (faces[k].left(),faces[k].bottom() + 5)
                #防止重复插入
                # hasName = False
                # for recindex in range(len(self.recList)):
                #     if self.recList[recindex].name == name_namelist[k]:
                #         hasName = True
                # if hasName is False :
                for recindex in range(len(self.recList)):
                    if self.recList[recindex].name == name_namelist[k]:
                        self.recList.pop(recindex)
                        break
                face = FaceData(name= name_namelist[k],data=self.features_known_arr[i])
                self.recList.append(face)
                self.topInfoFunc(len(faces),",".join(name_namelist))
                # print("features_known_arr same...")
                # 姓名列表
                self.knownlist = name_namelist
                self.postion = pos_namelist
        print("allForCSV..........");
    def removeCap(self):
        # self.colse = True
        # 释放摄像头
        self.cap.release()