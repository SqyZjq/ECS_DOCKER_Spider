#基于信息摘要算法进行数据的去重判断和存储

#1.基王内存的存健
#2.基于redis的存储’
#3.基于mysql的存储
import hashlib


class BaseFilter(object):
    # 基于信息摘要算法进行数据的去重判断和存储
    def __init__(self,hash_func_name="md5",redis_host="localhost",redis_port=6379 ,redis_db = 0,redis_key = "filter",mysql_url=None,mysql_table_name = "filter"):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis_key = redis_key
        self.mysql_url = mysql_url
        self.mysql_table_name = mysql_table_name
        self.hash_func= getattr(hashlib,hash_func_name)
        self.storage = self._get_storage()

    def _get_storage(self):
        """
        获取存储对象
        :return:
        """
        pass
    def _safe_data(self,data):
        """
        :param data: 给定的原始数据
        :return: 二进制字符串
        """
        if isinstance(data,bytes):
            return data
        elif isinstance(data,str):
            return data.encode()
        else:
            raise Exception("请提供一个字符串")

    def _get_hash_value(self,data):
        """
        根据给定的数据，返回的对应信息摘要hash值
        :param data: 给定的原始数据（二进制类型的字符串数据）
        :return: hash值
        """
        hash_obj = self.hash_func()
        hash_obj.update(self._safe_data(data))
        hash_value = hash_obj.hexdigest()
        return hash_value
    def save(self,data):
        """
        根据data计算出对应的指纹进行存储
        :param data: 给定的原始数据（二进制类型的字符串数据）
        :return:存储结果
        """
        hash_value = self._get_hash_value(data)
        self._save(hash_value)
        return hash_value
    def _save(self,hash_value):
        """
        将hash_value存储到相应的地方
        交给对应的子类去继承
        :param hash_value: 信息摘要hash值
        :return: 存储结果
        """
        pass
    def is_exists(self,data):
        """
        判断给定的数据对应的指纹是否存在
        :param data:给定的原始数据（二进制类型的字符串数据）
        :return: True of False
        """
        hash_value = self._get_hash_value(data)
        return  self._is_exists(hash_value)
    def _is_exists(self,hash_value):
        """
        判断给定的数据对应的指纹是否存在
        交给对应的子类去继承
        :param hash_value: 信息摘要hash值
        :return: True of False
        """
        pass



