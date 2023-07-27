from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
image_face_fusion = pipeline(Tasks.image_face_fusion, model='damo/cv_unet-image-face-fusion_damo')