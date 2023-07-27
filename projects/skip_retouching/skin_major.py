from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from data import filepath as fp
from base.media_base import BaseClass
class Fix_Photo(BaseClass):

    def __init__(self):
        super().__init__()
        self.model = pipeline(Tasks.skin_retouching,model='damo/cv_unet_skin-retouching')



if __name__ == '__main__':
    fip = Fix_Photo()
    a = fip.process_image(fp.FILE_TEST.FACE1)
    fip.process_video(fp.FILE_TEST.VIDEO_13S)
    print(a)