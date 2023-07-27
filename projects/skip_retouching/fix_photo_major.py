from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from data import filepath as fp
from base.media_base import BaseClass
class Fix_Photo(BaseClass):

    def __init__(self):
        super().__init__()
        self.model = pipeline(Tasks.image_portrait_enhancement, model='damo/cv_gpen_image-portrait-enhancement')
        self.scaling = 2


if __name__ == '__main__':
    fip = Fix_Photo()
    #fip.process_image(fp.FILE_TEST.FACE1)
    fip.process_video(fp.FILE_TEST.VIDEO_13S)
