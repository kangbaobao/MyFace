'''当一个队列为空的时候，用get取回堵塞
所以一般取队列的时候会用，get_nowait()方法
这个方法在向一个空队列取值的时候会抛一个Empty异常，
所以一般会先判断队列是否为空，如果不为空则取值；'''
from multiprocessing import Process, Queue
from queue import Empty
import os
import pandas as pd  # 数据处理的库 Pandas
import json
import math
#进入的队列
qInput = Queue()
# 出来的队列
qOutput = Queue()
cPrcess = None
# isRun = True
# 处理数据  qInput 存放的格式 [从图像识别到的人脸列表，人脸总列表] qOutput 存放的是是识别到的 FaceData列表
def handlerProcess(qInput,qOutput):
    from .FaceRecongnition import return_euclidean_distance
    print("in child:")#
    path = os.path.join('data','data_dlib','dlib_face_recognition_resnet_model_v1.dat')
    # 处理存放所有人脸特征的 csv
    path_features_known_csv = os.path.join('data','features_all.csv')#
    csv_rd = pd.read_csv(path_features_known_csv, header=None)

    # 用来存放所有录入人脸特征的数组
    features_known_arr = []
    # 读取已知人脸数据
    for i in range(csv_rd.shape[0]):
        features_someone_arr = []
        for j in range(0, len(csv_rd.ix[i, :])):
            features_someone_arr.append(csv_rd.ix[i, :][j])
            features_known_arr.append(features_someone_arr)
        print("Faces in Database：", features_known_arr)
    # 加载姓名列表
    load_list = []
    jsonpath = os.path.join('data','user.json')
    with open(jsonpath, 'r') as load_f:
        load_list = json.load(load_f)
    from .FaceRecongnition import DATANOFACE

    while True:
        # print("isRun: ",True)
        try:
            ele = qInput.get(block=True, timeout=2)
            for i in range(len(features_known_arr)):
                # 将某张人脸与存储的所有人脸数据进行比对
                compare = return_euclidean_distance(ele, features_known_arr[i])
                if compare == "same":  # 找到了相似脸
                    #总共一个人有128个特征点 所以i/128向下取整就是 这个的的index
                    index = math.floor(i/128.0)
                    name_name = load_list[index]
                    qOutput.put({"name":name_name,"data":features_known_arr[i]})
                    print("shibie :",name_name)

                else:
                    print("DATANOFACE :",DATANOFACE)
                    # qOutput.put({"name":DATANOFACE,'data':[x*0 for x in range(128)]})
        except Empty:
            pass
            # print(" ".join([]))
            # print("Queue has been empty.....")
        finally:
            pass
              # print("ele : ",ele)
#创建进程
def runProcess():
    #创建子进程
    customProcess = Process(target=handlerProcess, args=(qInput,qOutput))
    customProcess.start()
    # customProcess.join()
    cPrcess = customProcess

'''当一个队列为空的时候，用get取回堵塞
所以一般取队列的时候会用，get_nowait()方法
这个方法在向一个空队列取值的时候会抛一个Empty异常，
所以一般会先判断队列是否为空，如果不为空则取值；'''