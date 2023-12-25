from redis_queue.priority_redis_queue import PriorityRedisQueue

pqueue = PriorityRedisQueue("pqueue",host="172.18.0.2",db=15)
pqueue.put((1,"111"))
print(pqueue.get())