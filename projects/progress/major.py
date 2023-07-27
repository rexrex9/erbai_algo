from base import redis_base


RQ = redis_base.RedisQueue()
def run(trace_id,project_name):
    m = RQ.get_progress(trace_id,project_name)
    n,p=m.split(';')
    return n,p

if __name__ == '__main__':
    print(run('test','wav2lip'))