import pickle

from .base import BaseRedisQueue

class PriorityRedisQueue(BaseRedisQueue):
    """
    利用 redis的有序集合来实现数据的存取
    """
    def qsize(self):
        self.last_qsize = self.redis.zcard(self.name)
        return self.last_qsize
    def put_nowait(self, obj):
        if self.lazy_limit and self.last_qsize < self.maxsize:
            pass
        elif self.full():
            raise self.Full
        self.last_qsize = self.redis.zadd(self.name,obj[0],pickle.dumps(obj[1]))
        return True
    def get_nowait(self):
        """
        -1,-1:表示获取权重最大的数据
        0,0:表示获取权重最小的数据
        从有序集合中获取优先级最高的数据
        :return:
        """
        ret = self.redis.zrange(self.name,0,0)
        self.redis.zrem(self.name,ret[0])
        if ret is None:
            raise self.Empty
        return pickle.loads(ret[0])