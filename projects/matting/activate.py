from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
portrait_matting = pipeline(Tasks.portrait_matting,model='damo/cv_unet_image-matting')
video_matting = pipeline(Tasks.video_human_matting,model='damo/cv_effnetv2_video-human-matting')
universal_matting = pipeline(Tasks.universal_matting,model='damo/cv_unet_universal-matting')