# 布隆过滤器 redis版本实现

#1.多个hash函数的实现和求值
#2. hasn表实现和实现对应的映射和判断


import hashlib
import redis


class MultipleHash(object):
    def __init__(self, salts, hash_func_name="md5"):
        """
        初始化
        :param salts: 盐值列表
        """
        self.hash_func = getattr(hashlib, hash_func_name)
        if len(salts) <3:
            raise Exception("请提供至少提供3个salt")
        self.salts = salts

    def get_hash_value(self, data):
        """
        计算多个hash值
        :param data: 数据
        :return: hash值列表
        """
        hash_values = []
        for salt in self.salts:
            hash_obj = self.hash_func()
            hash_obj.update(self._safe_data(data))
            hash_obj.update(self._safe_data(str(salt)))  # 转换salt为字符串
            ret = hash_obj.hexdigest()
            hash_values.append(int(ret, 16))
        return hash_values

    def _safe_data(self, data):
        """
        :param data: 给定的原始数据
        :return: 二进制字符串
        """
        if isinstance(data, bytes):
            return data
        elif isinstance(data, str):
            return data.encode()
        else:
            raise Exception("请提供一个字符串或字节序列")


class BloomFilter(object):
    def __init__(self,salts,redis_host = 'localhost',redis_port = '6379',redis_db = 0,redis_key = 'bloomfilter'):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis_key = redis_key
        self.clent = self.get_redis_client()
        self.multiple_hash = MultipleHash(salts)

    def get_redis_client(self):
        '''
        返回一个redis的链接对象
        :return:
        '''
        pool = redis.ConnectionPool(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        client = redis.StrictRedis(connection_pool=pool)
        return client

    def save(self,data):
        '''
        将原始数据在hash表中一一映射 返回对应的偏移量
        :param data:
        :return:
        '''
        hash_values = self.multiple_hash.get_hash_value(data)
        offsets = []
        for hash_value in hash_values:
            offset = self._get_offset(hash_value)
            offsets.append(offset)
            self.clent.setbit(self.redis_key,offset,1)
        return offsets
    def _get_offset(self,hash_value):
        return hash_value % ( 2**9*2**20*2*8 )
    def is_exist(self,data):
        hash_values = self.multiple_hash.get_hash_value(data)
        bit_values = []
        for hash_value in hash_values:
            offset = self._get_offset(hash_value)
            v = self.clent.getbit(self.redis_key,offset)
            if v == 0:
                return False
            bit_values.append(v)
        if 0 in bit_values:
            return False
        return True

try:
    if __name__ == '__main__':
        data = ["987", "854", "ahshahsg", "1234567893", "678", "345", "ahshahsg"]
        bm = BloomFilter(salts=['1', '2', '3', '4'], redis_host='172.18.0.2')
        for d in data:
            if not bm.is_exist(d):
                bm.save(d)
                print("映射数据成功", d)
            else:
                print("发现重复数据", d)
except Exception as e:
    print(f"程序运行出错: {e}")

