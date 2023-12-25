from request_manager.utils.filiter_class.information_summary_filter import MySQLFilter

# filter = MemoryFilter()
# filter = RedisFilter(redis_host="172.17.0.3")
mysql_table_name = "mysql_table_name"  # 将此处替换为你的表名
mysql_url = "mysql+pymysql://root:password@172.17.0.5:3306/test?charset=utf8"
filter = MySQLFilter(mysql_url=mysql_url,mysql_table_name=mysql_table_name)
data = ["111","qwe","222","333","111","qwe","中文"]
for d in data:
   if filter.is_exists(d):
       print("发现重复的数据:",d)
   else:
       filter.save(d)
       print("保存去重的数据:",d)