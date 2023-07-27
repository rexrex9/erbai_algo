from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from data import filepath as fp
from os.path import join as osp
from uuid import uuid4
from base import oss_base,redis_base
class NoiseReduce():

    def __init__(self):
        self.project_name = 'noise_reduce'
        self.ans = pipeline(
            Tasks.acoustic_noise_suppression,
            model='damo/speech_frcrn_ans_cirm_16k')
        self.rq = redis_base.RedisQueue()

    def do(self, trace_id,audio_path,format='wav',ifoss=False):
        project_path = osp(fp.RESULTS.AUDIO_DIR, self.project_name)
        output_path = osp(project_path, str(uuid4()) + '.'+format)
        self.ans(audio_path,output_path=output_path)
        if ifoss:
            output_path = oss_base.upload(self.project_name, format, output_path)
        self.rq.add_progress(self.project_name, trace_id, 100, output_path)
        return output_path






if __name__ == '__main__':
    NR = NoiseReduce()
    NR.do(audio_path=fp.FILE_TEST.NOISE_WAV)