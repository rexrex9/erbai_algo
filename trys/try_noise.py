# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import requests


audio_path = 'algo_medias/test_files/reduce_noise.wav'
host = 'http://192.168.1.3'
host = 'http://112.124.67.138'

def try_skip_image():
    url = host +':9912/do'
    d = {'oss_media_path':audio_path,'out_format':'wav','ifoss':True}
    r = requests.post(url,json=d)
    print(r)
    print(r.json())

def try_skip_hello():
    url = host +':9912/hello'
    r = requests.get(url)
    print(r)
    print(r.text)

if __name__ == '__main__':
    try_skip_hello()
    try_skip_image()
    #try_skip_video()