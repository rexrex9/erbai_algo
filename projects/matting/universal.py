from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from base.media_base import BaseClass
from data import filepath as fp
from projects.matting.backgroud import BackGround
from PIL import Image
from os.path import join as osp
from uuid import uuid4
from utils import image_utils as iu
import os
class Universal(BaseClass):

    def __init__(self):
        super().__init__()
        self.model = pipeline(Tasks.universal_matting,model='damo/cv_unet_universal-matting')
        self.BG = BackGround()
        self.project_name='matting'

    def process_image(self, img_path, bg_path=None, ifbg=True,format='png'):
        img = iu.read_image(img_path)
        result = self.do_image(img)

        if ifbg:
            temp_path = osp(fp.TEMP.IMAGE_DIR, str(uuid4()) + '.' + format)
            iu.save_image(temp_path, result)
            img = self.BG.put_together(temp_path, bg_path)
            path = self.get_path_name(format)
            img.save(path)
            os.remove(temp_path)
            return path
        else:
            path = self.get_path_name(format)
            iu.save_image(path, result)
            return path


if __name__ == '__main__':
    fip = Universal()
    fip.process_image('a.png')

    # from modelscope.outputs import OutputKeys
    # import cv2
    # universal_matting = pipeline(Tasks.universal_matting,model='damo/cv_unet_universal-matting')
    # result = universal_matting('https://modelscope.oss-cn-beijing.aliyuncs.com/demo/image-matting/1.png')
    # cv2.imwrite('result.png', result[OutputKeys.OUTPUT_IMG])