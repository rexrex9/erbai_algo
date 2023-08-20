
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


'''
0%;Traceback (most recent call last):
  File "D:\workspace\pythonworkspace\newonline\digitalperson\erbai_algo\projects\matting\index.py", line 22, in _do
    result_path = M.do(trace_id,media_path,type,ifbg,bg_medio_path,out_format,ifoss,temp_audio_path)
  File "D:\workspace\pythonworkspace\newonline\digitalperson\erbai_algo\projects\matting\main.py", line 19, in do
    result_path = self._run(media_path,type,trace_id,ifbg,bg_medio_path,out_format,audio_path=audio_path)
  File "D:\workspace\pythonworkspace\newonline\digitalperson\erbai_algo\projects\matting\main.py", line 65, in _run
    out_path = self.hum_vid.process_png_list(trace_id,tmp_png_dir,audio_path=audio_path,bg_img=bg_img_path,bg_video=bg_video_path)
  File "D:\workspace\pythonworkspace\newonline\digitalperson\erbai_algo\projects\matting\human_video.py", line 116, in process_png_list
    output_path = self.put_video_and_voice_together(temp_output_path, audio_path)
  File "D:\workspace\pythonworkspace\newonline\digitalperson\erbai_algo\base\media_base.py", line 114, in put_video_and_voice_together
    audio = mpe.AudioFileClip(temp_audio_path)
  File "C:\Users\50425\home\work\program\env\envs\modelscopre\lib\site-packages\moviepy\audio\io\AudioFileClip.py", line 70, in __init__
    self.reader = FFMPEG_AudioReader(filename, fps=fps, nbytes=nbytes,
  File "C:\Users\50425\home\work\program\env\envs\modelscopre\lib\site-packages\moviepy\audio\io\readers.py", line 51, in __init__
    infos = ffmpeg_parse_infos(filename)
  File "C:\Users\50425\home\work\program\env\envs\modelscopre\lib\site-packages\moviepy\video\io\ffmpeg_reader.py", line 244, in ffmpeg_parse_infos
    is_GIF = filename.endswith('.gif')
AttributeError: 'NoneType' object has no attribute 'endswith'
'''