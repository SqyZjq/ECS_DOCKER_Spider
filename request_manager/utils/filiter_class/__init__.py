def get_filiter_class(cls_name):
    if cls_name == "redis":
        from .information_summary_filter.redis_filter import RedisFilter  # 假设这是类名
        return RedisFilter
    elif cls_name == "mysql":
        from .information_summary_filter.mysql_filter import MysqlFilter  # 假设这是类名
        return MysqlFilter
    elif cls_name == "memory":
        from .information_summary_filter.memory_filter import MemoryFilter
        return MemoryFilter
    elif cls_name == "bloom":
        from .bloomfilter import BloomFilter
        return BloomFilter
