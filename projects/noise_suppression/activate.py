from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
ans = pipeline(Tasks.acoustic_noise_suppression,model='damo/speech_frcrn_ans_cirm_16k')