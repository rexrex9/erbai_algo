# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import requests


face_path = 'algo_medias/test_files/face1.jpg'
video_path = 'algo_medias/test_files/test_video_13s.mp4'
host = 'http://172.17.0.2'
#host = 'http://116.62.176.131'
host = 'http://120.26.104.180'
def try_skip_image():
    url = host +':9911/do'
    d = {'oss_media_path':video_path,'face_path':face_path,'out_format':'mp4','ifoss':True}
    r = requests.post(url,json=d)
    print(r)
    print(r.json())


def try_skip_hello():
    url = host +':9911/hello'
    r = requests.get(url)
    print(r)
    print(r.text)

if __name__ == '__main__':
    try_skip_hello()
    try_skip_image()
    #try_skip_video()

