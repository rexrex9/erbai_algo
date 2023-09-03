import os
from modelscope.outputs import OutputKeys
import moviepy.editor as mpe
import cv2
from utils import image_utils as iu
from data import filepath as fp
from os.path import join as osp
from uuid import uuid4
from PIL import Image
from base.redis_base import RedisQueue

class BaseClass():

    def __init__(self):
        self.project_name = None
        self.model=None
        self.scaling = 1
        self.rq = RedisQueue()

    def get_format(self,path):
        return path.split('.')[-1]

    def get_path_name(self,format='mp4'):
        if format=='mp4':
            project_path = osp(fp.RESULTS.VIDEO_DIR,self.project_name )
            file_path = osp(project_path, str(uuid4()) + '.' + format)
        elif format=='png_list':
            project_path = osp(fp.RESULTS.PNG_LIST_DIR, self.project_name)
            file_path = osp(project_path, str(uuid4()))
            if not os.path.exists(file_path):
                os.makedirs(file_path)
        else:
            project_path = osp(fp.RESULTS.IMAGE_DIR, self.project_name)
            file_path = osp(project_path, str(uuid4()) + '.' + format)

        if not os.path.exists(project_path):
            os.makedirs(project_path)

        return file_path

    def _clean_temp(self,temp_audio_path,temp_video_path):
        os.remove(temp_audio_path)
        os.remove(temp_video_path)

    def process_video(self, trace_id,video_path,face_img=None,format='mp4'):
        if format=='png_list':
            result_video_path =  self._seq_do_video(trace_id,video_path,face_img,format='png_list')
        else:
            temp_audio_path = self._seq_voice(video_path)
            temp_video_path = self._seq_do_video(trace_id,video_path,face_img)
            result_video_path = self.put_video_and_voice_together(temp_video_path, temp_audio_path,format)
            self._clean_temp(temp_audio_path, temp_video_path)
        return result_video_path
    def process_image(self,face_path,image_path=None,format='jpg'):
        face_img = iu.read_image(face_path)
        if image_path:
            img = iu.read_image(image_path)
        else:
            img = None
        img = self.do_image(face_img,img)
        out_path = self.get_path_name(format)
        iu.save_image(out_path, img)
        return out_path

    def _seq_voice(self,video_path):
        video = mpe.VideoFileClip(video_path)
        audio = video.audio
        temp_audio_path = osp(fp.TEMP.AUDIO_DIR, str(uuid4()) + '.mp3')
        audio.write_audiofile(temp_audio_path)
        return temp_audio_path

    def _seq_do_video(self,trace_id,video_path,face_img=None,format='mp4'):
        cap = cv2.VideoCapture(video_path)
        if format=='png_list':
            temp_video_path = self.get_path_name(format)
        else:
            temp_video_path = osp(fp.TEMP.VIDEO_DIR, str(uuid4()) + '.avi')

            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            videoWriter = cv2.VideoWriter(temp_video_path, cv2.VideoWriter_fourcc(*'XVID'), fps,
                                          (width * self.scaling, height * self.scaling))

        if face_img:
            face_img = iu.read_image(face_img)

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        count = 0
        while True:
            print('{}/{}'.format(count, total_frames))
            ret, frame = cap.read()
            if not ret: break
            if face_img:
                #ndarray转换为PIL.Image
                frame = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
                img = self.do_image(face_img,frame)
            else:
                img = self.do_image(frame)
            if format=='png_list':
                out_path = osp(temp_video_path,'{}.png'.format(count))
                iu.save_image(out_path, img)
            else:
                videoWriter.write(img)
            count += 1
            print(round(count/total_frames,3)*100-1)
            self.rq.add_progress(self.project_name,trace_id,round(count/total_frames,3)*100-1)
        cap.release()
        if format!='png_list':
            videoWriter.release()
        return temp_video_path

    def put_video_and_voice_together(self,temp_video_path,temp_audio_path,format='mp4'):
        video = mpe.VideoFileClip(temp_video_path)
        audio = mpe.AudioFileClip(temp_audio_path)
        video = video.set_audio(audio)
        result_video_path = self.get_path_name(format)
        video.write_videofile(result_video_path)
        return result_video_path

    def do_image(self, img,timg=None):
        result = self.model(img)
        return result[OutputKeys.OUTPUT_IMG]

