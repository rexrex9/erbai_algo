
from uuid import uuid4
from db import oss_conn
import shutil
import os
from data import filepath as fp
from PIL import Image

ROOT_DIR = 'algo_medias'
IMAGE_OSS = 'image'
VIDEO_OSS = 'video'
AUDIO_OSS = 'audio'
PNG_LIST_OSS ='png_list'

OC = oss_conn.OssConn()

def genrate_oss_path(project_name,format):
    if format == 'png':
        return ROOT_DIR +'/'+ IMAGE_OSS+'/'+ project_name + '/' + str(uuid4()) + '.png'
    elif format == 'mp4':
        return ROOT_DIR +'/'+ VIDEO_OSS+'/'+ project_name + '/' + str(uuid4()) + '.mp4'
    elif format == 'png_list':
        return ROOT_DIR +'/'+ PNG_LIST_OSS+'/'+ project_name + '/' + str(uuid4())
    elif format in ['mp3','wav']:
        return ROOT_DIR +'/'+ AUDIO_OSS+'/'+ project_name + '/' + str(uuid4()) + '.' + format

def genrate_temp_path(format):
    format=format.lower()
    if format in ['png','jpg','jpeg']:
        return fp.TEMP.IMAGE_DIR + '/' + str(uuid4()) + '.' + format
    elif format in ['mp4','avi','mov']:
        return fp.TEMP.VIDEO_DIR + '/' + str(uuid4()) + '.' +  format
    elif format in ['mp3','wav']:
        return fp.TEMP.AUDIO_DIR+'/' + str(uuid4()) + '.' + format
    else:
        return fp.TEMP.PNG_LIST_DIR + '/' + str(uuid4())+'.'+format

def save_temp_file(project_name,format,file):
    #file是二进制文件
    temp_path = genrate_temp_path(project_name, format)
    if format in ['png','jpg','jpeg']:
        #保存图片
        img = Image.open(file)
        img.save(temp_path)
    elif format in ['mp4','avi','mov']:
        #保存视频
        with open(temp_path,'wb') as f:
            f.write(file)
    else:
        #保存音频
        with open(temp_path,'wb') as f:
            f.write(file)
    return temp_path

def upload(project_name, out_format,file_path):
    oss_path = genrate_oss_path(project_name, out_format)
    if out_format == 'png_list':
        OC.upload_dir(file_path, oss_path)
        shutil.rmtree(file_path)
    else:
        print(file_path)
        print(oss_path)
        OC.upload(file_path, oss_path)
        os.remove(file_path)
    return oss_path


def download(oss_path):
    format = oss_path.split('.')[-1]
    temp_path = genrate_temp_path(format)
    OC.download(oss_path, temp_path)
    return temp_path


if __name__ == '__main__':
    pass


