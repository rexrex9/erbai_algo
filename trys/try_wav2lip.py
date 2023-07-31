# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import requests

face_path = 'algo_medias/test_files/face1.jpg'
video_path = 'algo_medias/test_files/test_video_13s.mp4'
audio_path = 'algo_medias/test_files/wav2lip_audio.WAV'
host = 'http://172.17.0.3'
#host = 'http://116.62.176.131'
def try_image():
    url = host +':8999/do'
    d = {'oss_media_path':face_path,'audio_path':audio_path,'out_format':'png','ifoss':True}
    r = requests.post(url,json=d)
    print(r)
    print(r.json())

def try_video():
    url = host +':8999/do'
    d = {'oss_media_path':video_path,'audio_path':audio_path,'out_format':'mp4','ifoss':True}
    r = requests.post(url,json=d)
    print(r)
    print(r.json())

def try_hello():
    url = host +':8999/hello'
    r = requests.get(url)
    print(r)
    print(r.text)

if __name__ == '__main__':
    try_hello()
    #try_video()
    try_video()