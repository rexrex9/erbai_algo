from db.redis_db import Redis
from uuid import uuid4

class RedisQueue(object):


    ROOT_PREFIX = 'ALGO:'
    def __init__(self):
        self.redis_conn = Redis().r

    def init_progress(self,project_name):
        trace_id = str(uuid4())
        topic_name = self.ROOT_PREFIX + project_name + ':' + trace_id
        self.redis_conn.lpush(topic_name, '0%;init')
        self.redis_conn.expire(topic_name, 86400 * 2)  # 设置过期时间为2天
        return trace_id

    def add_progress(self,project_name, trace_id, progress,msg='processing'):
        topic_name = self.ROOT_PREFIX + project_name + ':' + trace_id
        self.redis_conn.lpush(topic_name, '{}%;{}'.format(progress,msg))

    def get_progress(self,trace_id,project_name):
        topic_name = self.ROOT_PREFIX + project_name + ':' + trace_id
        ls =  self.redis_conn.lrange(topic_name, 0, 0)
        return ls[0] if len(ls)>0 else None
