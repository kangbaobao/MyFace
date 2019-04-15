# 从人脸图像文件中提取人脸特征存入 CSV
import cv2
import os
import dlib
from skimage import io
import csv
import numpy as np
import pandas as pd
from FilesUtils import path_csv_from_photos,path_photos_from_camera
import json

class FaceToCSV(object):
    def __init__(self,person_names='',writeOutput=None):
        self.writeOutput = writeOutput
        self.person_names =  person_names
        # Dlib 正向人脸检测器
        self.detector = dlib.get_frontal_face_detector()
        # Dlib 人脸预测器
        spath = os.path.join("data","data_dlib","shape_predictor_68_face_landmarks.dat")
        self.predictor = dlib.shape_predictor(spath)
        # "data/data_dlib/shape_predictor_68_face_landmarks.dat"
        # Dlib 人脸识别模型
        # Face recognition model, the object maps human faces into 128D vectors
        fpath = os.path.join("data","data_dlib","dlib_face_recognition_resnet_model_v1.dat")
        self.facerec = dlib.face_recognition_model_v1(fpath)
        # "data\\data_dlib\\dlib_face_recognition_resnet_model_v1.dat"
        self.readAnySome()
    # 读取某人所有的人脸图像的数据，写入 person_X.csv
    def readAnySome(self):
        faces = os.listdir(path_photos_from_camera)
        # faces.sort()
        for person in faces:
            print("##### " + person + " #####")
            # print(path_csv_from_photos + person + ".csv")
            #  当前人时，才读取
            # if person == self.person_names:
            cpath = os.path.join(path_photos_from_camera,person)
            ppath = os.path.join(path_csv_from_photos,person + ".csv")
            print("readAnySome ppath :",ppath);
            self.write_into_csv(cpath, ppath)
    # 返回单张图像的 128D 特征
    def return_128d_features(self,path_img):
        img = io.imread(path_img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces = self.detector(img_gray, 1)
        print("检测到人脸的图像：", path_img, "\n")
        # 因为有可能截下来的人脸再去检测，检测不出来人脸了
        # 所以要确保是 检测到人脸的人脸图像 拿去算特征
        if len(faces) != 0:
            shape = self.predictor(img_gray, faces[0])
            face_descriptor = self.facerec.compute_face_descriptor(img_gray, shape)
        else:
            face_descriptor = 0
            print("no face")
        # print(face_descriptor)
        return face_descriptor

    # 将文件夹中照片特征提取出来, 写入 CSV
    #   path_faces_personX:     图像文件夹的路径
    #   path_csv_from_photos:   要生成的 CSV 路径
    def write_into_csv(self,path_faces_personX, path_csv_from_photos):
        photos_list = os.listdir(path_faces_personX)
        with open(path_csv_from_photos, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            print("writer :",type(writer))
            if photos_list:
                for i in range(len(photos_list)):
                    # 调用return_128d_features()得到128d特征
                    # print()
                    info = "正在读的人脸图像："+ path_faces_personX + "/" + photos_list[i]
                    self.writeOutput(info)
                    features_128d = self.return_128d_features(path_faces_personX + "/" + photos_list[i])
                    #  print(features_128d)
                    # 遇到没有检测出人脸的图片跳过
                    if features_128d == 0:
                        i += 1
                        # self.writeOutput("{0}这张图片没有读出人脸数据".format(path_faces_personX + "/" + photos_list[i]))
                    else:
                        writer.writerow(features_128d)
            else:
                self.writeOutput("你的截图文件夹没有图片，请重新截取")
                print("Warning: Empty photos in " + path_faces_personX + '/')
                writer.writerow("")

    # 从 CSV 中读取数据，计算 128D 特征的均值
    def compute_the_mean(self,path_csv_from_photos):
        column_names = []

        # 128D 特征
        for feature_num in range(128):
            column_names.append("features_" + str(feature_num + 1))
        print("compute_the_mean : ",path_csv_from_photos)
        # 利用 pandas 读取 csv
        f = open(path_csv_from_photos)
        rd = pd.read_csv(f, names=column_names)
        # rd = pd.read_csv(path_csv_from_photos, names=column_names)

        if rd.size != 0:
            # 存放 128D 特征的均值
            feature_mean_list = []

            for feature_num in range(128):
                tmp_arr = rd["features_" + str(feature_num + 1)]
                tmp_arr = np.array(tmp_arr)
                # 计算某一个特征的均值
                tmp_mean = np.mean(tmp_arr)
                feature_mean_list.append(tmp_mean)
        else:
            feature_mean_list = []
        return feature_mean_list

    def WriteCSV(self):
        # 存放所有特征均值的 CSV 的路径
        cvspath = os.path.join('data','features_all.csv')
        path_csv_from_photos_feature_all = cvspath#"data/features_all.csv"
        with open(path_csv_from_photos_feature_all, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            csv_rd = os.listdir(path_csv_from_photos)
            csv_rd.sort()
            csv_strarr = [ cstr.split('.')[0] for cstr in csv_rd]
            # 将用户名列表转化成json保存在文件中 与 features_all.csv 的顺序保持一致，
            # 人脸识别时，就可以通过对应的位置来查找用户名了
            userpath = os.path.join('data','user.json')
            with open(userpath, "w") as f:
                json.dump(csv_strarr, f)
                print("加载入文件完成...")
                self.writeOutput("用户信息录入中....")
            print("##### 得到的特征均值 / The generated average values of features stored in: #####")
            for i in range(len(csv_rd)):
                # if csv_rd[i].split('.')[0] == self.person_names:
                path = os.path.join(path_csv_from_photos,csv_rd[i])
                feature_mean_list = self.compute_the_mean(path)
                print(path_csv_from_photos + csv_rd[i])
                writer.writerow(feature_mean_list)
            self.writeOutput("人脸数据录入完成....")