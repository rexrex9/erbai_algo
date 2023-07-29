from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys
from data import filepath as fp
from base.media_base import BaseClass
from base import oss_base,redis_base
class Photo(BaseClass):

    def __init__(self):
        super().__init__()
        self.fix_model = pipeline(Tasks.image_portrait_enhancement, model='damo/cv_gpen_image-portrait-enhancement')
        self.skin_model = pipeline(Tasks.skin_retouching, model='damo/cv_unet_skin-retouching')
        self.scaling = 2
        self.project_name = 'fix_photo'

    def do_image(self,img,timg=None):
        img = self.skin_model(img)[OutputKeys.OUTPUT_IMG]
        img = self.fix_model(img)[OutputKeys.OUTPUT_IMG]
        return img


class Major():

    def __init__(self):
        self.P = Photo()
        self.rq = redis_base.RedisQueue()
        self.project_name = self.P.project_name

    def do(self,trace_id,media_path,output_format,ifoss=False):
        media_format = self.P.get_format(media_path)
        if media_format in ['mp4','mov']:
            outpath = self.P.process_video(trace_id,media_path,format=output_format)
        else:
            outpath = self.P.process_image(media_path,format=output_format)

        if ifoss:
            outpath = oss_base.upload(self.P.project_name, output_format, outpath)
        self.rq.add_progress(self.project_name, trace_id, 100, outpath)
        return outpath


if __name__ == '__main__':
    fip = Major()
    #fip.do('t1',fp.FILE_TEST.FACE1,'png')
    fip.do('t1',fp.FILE_TEST.VIDEO_13S,'png_list')