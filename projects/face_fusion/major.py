
from base.media_base import BaseClass
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from data import filepath as fp
from base import oss_base,redis_base
class FaceFustion(BaseClass):

    def __init__(self):
        super().__init__()
        self.model=pipeline(Tasks.image_face_fusion,model='damo/cv_unet-image-face-fusion_damo')
        self.project_name = 'face_fusion'

    def _do_image(self,img,timg=None):
        return self.model(dict(template=timg, user=img))[OutputKeys.OUTPUT_IMG]

class Major():

    def __init__(self):
        self.P = FaceFustion()
        self.rq = redis_base.RedisQueue()
        self.project_name = self.P.project_name
    def do(self,trace_id,media_path,face_path,output_format,ifoss=False):
        media_format = self.P.get_format(media_path)
        if media_format in ['mp4','mov']:
            outpath = self.P.process_video(trace_id,media_path,face_path,format=output_format)
        else:
            outpath = self.P.process_image(media_path,face_path,format=output_format)
        if ifoss:
            outpath = oss_base.upload(self.P.project_name, output_format, outpath)

        self.rq.add_progress(self.project_name, trace_id, 100, outpath)
        return outpath

if __name__ == '__main__':
    fip = FaceFustion()
    #a = fip.process_image(fp.FILE_TEST.FACE1,fp.FILE_TEST.FACE2)
    #print(a)
    a = fip.process_video(fp.FILE_TEST.VIDEO_13S,fp.FILE_TEST.FACE1)
    print(a)
    # image_face_fusion = pipeline(Tasks.image_face_fusion,model='damo/cv_unet-image-face-fusion_damo')
    # template_path = 'https://modelscope.oss-cn-beijing.aliyuncs.com/test/images/facefusion_template.jpg'
    # user_path = 'https://modelscope.oss-cn-beijing.aliyuncs.com/test/images/facefusion_user.jpg'
    # result = image_face_fusion(dict(template=template_path, user=user_path))
    #
    # cv2.imwrite('result.png', result[OutputKeys.OUTPUT_IMG])
    # print('finished!')