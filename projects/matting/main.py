# -*- coding: utf-8 -*-
import shutil

from projects.matting import human_video,human_figure,universal
from base import oss_base
from base import redis_base
import zipfile

class Major():

    def __init__(self):
        self.hf_fig = human_figure.HumanFigure()
        self.hum_vid = human_video.HumanVideo()
        self.uni_fig = universal.Universal()
        self.project_name = 'matting'
        self.rq = redis_base.RedisQueue()

    def do(self,trace_id,media_path,type,ifbg=True,bg_medio_path=None,out_format='mp4',ifoss=True,audio_path=None):
        result_path = self._run(media_path,type,trace_id,ifbg,bg_medio_path,out_format,audio_path=audio_path)
        if ifoss:
            result_path = oss_base.upload(self.project_name,out_format,result_path)
        self.rq.add_progress(self.project_name,trace_id,100,result_path)
        return result_path

    def _run(self,media_path,type,trace_id,ifbg=True,bg_medio_path=None,out_format='mp4',audio_path=None):
        input_format = media_path.split('.')[-1]

        if type == 'human_figure':
            if input_format in ['png','jpg','jpeg']:
                out_path = self.hf_fig.process_image(media_path,bg_medio_path,ifbg=ifbg,format='png')
            else:
                raise Exception('input_format must be png or jpg or jpeg if type is human_figure')
        elif type == 'universal_figure':
            if input_format in ['png','jpg','jpeg']:
                out_path = self.hf_fig.process_image(media_path,bg_medio_path,ifbg=ifbg,format='png')
            else:
                raise Exception('input_format must be png or jpg or jpeg if type is universal_figure')
        elif type == 'human_video':
            if input_format in ['mp4','mov']:
                bg_video_path = bg_img_path = None
                if bg_medio_path:
                    bg_format = bg_medio_path.split('.')[-1]
                    if bg_format in ['mp4','mov']:
                        bg_video_path = bg_medio_path
                    else:
                        bg_img_path = bg_medio_path
                out_path = self.hum_vid.process_video(trace_id,media_path,bg_img=bg_img_path,bg_video=bg_video_path,format=out_format,ifbg=ifbg)
            else:
                raise Exception('input_format must be mp4 or mov if type is human_video')
        elif type=='png_list':
            if input_format not in ['zip']:
                raise Exception('input_format must be zip if type is png_list')
            bg_video_path = bg_img_path = None
            tmp_png_dir = oss_base.genrate_temp_path('png_list')
            # 读取压缩文件
            file = zipfile.ZipFile(media_path)
            file.extractall(tmp_png_dir)
            file.close()
            if bg_medio_path:
                bg_format = bg_medio_path.split('.')[-1]
                if bg_format in ['mp4', 'mov']:
                    bg_video_path = bg_medio_path
                else:
                    bg_img_path = bg_medio_path
            out_path = self.hum_vid.process_png_list(trace_id,tmp_png_dir,audio_path=audio_path,bg_img=bg_img_path,bg_video=bg_video_path)
            shutil.rmtree(tmp_png_dir)
        else:
            raise Exception('type must be human_figure or human_video or universal_figure')

        return out_path