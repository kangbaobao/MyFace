import os
import shutil
path_photos_from_camera = 'userimg'
path_csv_from_photos = 'usercvs'
# 新建保存人脸图像文件和数据CSV文件夹
def pre_work_mkdir(dir):
    # 新建文件夹
    if os.path.isdir(dir):
        pass
    else:
        os.mkdir(dir)
# 删除文件夹下的所有目录，
def deldir(dir):
    # 删除
    folders_rd = os.listdir(dir)
    for i in range(len(folders_rd)):
        shutil.rmtree(dir+folders_rd[i])