from base import redis_base
from base import docker_base
RQ = redis_base.RedisQueue()
def run(trace_id,project_name):
    m = RQ.get_progress(trace_id,project_name)
    n,p=m.split(';')
    return n,p


DOCKER_RUN_DICT = {
'wav2lip':'docker run -d --gpus all -p 8999:8999 -v /root/work/logs/wa2l:/app/major/logs -v /root/work/results/wav2lip_results:/app/major/data/results rexrex9/repo1:wa2l',
'fix_photo':'docker run -d --gpus all -p 9910:9910 -v /root/work/logs/skip:/app/logs -v /root/work/results/modelscope_results:/app/data/results rexrex9/repo1:skip',
'face_fusion':'docker run -d --gpus all -p 9911:9911 -v /root/work/logs/fusion:/app/logs -v /root/work/results/modelscope_results:/app/data/results rexrex9/repo1:fusion',
'matting':'docker run -d --gpus all -p 9909:9909 -v /root/work/logs/matting:/app/logs -v /root/work/results/modelscope_results:/app/data/results rexrex9/repo1:matting',
'noise_reduce':'docker run -d --gpus all -p 9912:9912 -v /root/work/logs/noise:/app/logs -v /root/work/results/modelscope_results:/app/data/results rexrex9/repo1:noise'
                   }

def docker_swith(task_name,openorclose):
    if openorclose:
        r = docker_base.docker_call(DOCKER_RUN_DICT[task_name])
        if r!=0:
            docker_base.docker_run(task_name)
    else:
        docker_base.docker_stop(task_name)





if __name__ == '__main__':
    #print(run('test','wav2lip'))
    docker_swith('redis',False)