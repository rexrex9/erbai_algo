from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from data import filepath as fp
from base.media_base import BaseClass
class Skin(BaseClass):

    def __init__(self):
        super().__init__()
        self.model = pipeline(Tasks.skin_retouching,model='damo/cv_unet_skin-retouching')
        self.project_name = 'fix_photo'



if __name__ == '__main__':
    fip = Skin()
    #a = fip.process_image(fp.FILE_TEST.FACE1)
    a = fip.process_video('a',fp.FILE_TEST.VIDEO_13S)
    print(a)