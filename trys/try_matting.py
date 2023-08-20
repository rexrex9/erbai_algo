

# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import requests

face_path = 'algo_medias/test_files/face1.jpg'
video_path = 'algo_medias/test_files/test_video_13s.mp4'
png_path = 'test/png_list_alpha.zip'
audio_path = 'algo_medias/test_files/wav2lip_audio.WAV'
host = 'http://172.17.0.2'
#host = 'http://116.62.176.131'
host = 'http://192.168.1.3'

def try_png_video():
    url = host +':9909/do'
    d = {'oss_media_path':png_path,'out_format':'mp4','ifoss':False,'type':'png_list','audio_path':audio_path}
    r = requests.post(url,json=d)
    print(r)
    print(r.json())

def try_skip_hello():
    url = host +':9909/hello'
    r = requests.get(url)
    print(r)
    print(r.text)

if __name__ == '__main__':
    try_skip_hello()
    #try_skip_image()
    try_png_video()
