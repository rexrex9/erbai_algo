

# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import requests

face_path = 'test/face1.jpg'
video_path = 'algo_medias/test_files/test_video_13s.mp4'
#png_path = 'test/png_list_alpha.zip'
png_path = 'creat_video/roles/luni02-60.zip,'
audio_path = 'audio/1608287747783532545/776183b4/f5196490-ada2-41b1-a1ad-7a5f87ec6cfc.wav'
host = 'http://172.17.0.2'
#host = 'http://114.55.129.121'
#host = 'http://192.168.1.3'
host = 'http://127.0.0.1'

def try_png_video():
    url = host +':9909/do'
    d = {'oss_media_path':png_path,'bg_media_path':'creat_video/videoSynthesis/1702647791917170690/d281125dc6afee4a2cfb24834c9882da.mp4','ifbg':True,
         'out_format':'mp4','ifoss':True,'type':'png_list','audio_path':audio_path}
    r = requests.post(url,json=d)
    print(r)
    print(r.json())

def try_skip_hello():
    url = host +':9909/hello'
    r = requests.get(url)
    print(r)
    print(r.text)

def try_skip_image():
    url = host +':9909/do'
    d = {'oss_media_path':face_path,'out_format':'png','ifoss':True,'type':'human_figure'}
    r = requests.post(url,json=d)
    print(r)
    print(r.json())


if __name__ == '__main__':
    try_skip_hello()
    #try_skip_image()
    try_png_video()
