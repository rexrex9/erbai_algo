from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
skin_retouching = pipeline(Tasks.skin_retouching,model='damo/cv_unet_skin-retouching')
portrait_enhancement = pipeline(Tasks.image_portrait_enhancement, model='damo/cv_gpen_image-portrait-enhancement')