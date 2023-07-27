
from redis import Redis as redis

class Redis():

    def __init__(self):
        host = 'r-bp17gbbpfudn8teu8gpd.redis.rds.aliyuncs.com'
        port = 6379
        username = 'rbyroot'
        password = 'Rby2022!'
        self.r = redis(host=host, port=port, decode_responses=True,password=password,username=username)


    def __del__(self):
        self.r.close()


if __name__ == '__main__':
    a = Redis().r.ping()
    print(a)
    r = Redis().r



    #
    # r.lpush('wav2lip:test', json.dumps([1,'a']))
    # # 设定过期时间5秒
    # r.expire('wav2lip:test', 5)
