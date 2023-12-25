# import re
# from simhash import Simhash
# def get_features(s):
#     width = 3
#     s = s.lower()
#     s = re.sub(r'[^\w]+', '', s)
#     ret=[s[i:i + width] for i in range(max(len(s) - width + 1, 1))]
#     print(ret)
#     return ret
#
# print('%x' % Simhash(get_features('How are you? I am fine. Thanks.')).value)
# print('%x' % Simhash(get_features('How are u? I am fine.     Thanks.')).value)
# print('%x' % Simhash(get_features('How r you?I    am fine. Thanks.')).value)
#
# print(Simhash(['how', 'owa', 'war', 'are', 'rey', 'eyo', 'you', 'oui', 'uia', 'iam', 'amf', 'mfi', 'fin', 'ine', 'net', 'eth', 'tha', 'han', 'ank', 'nks']).distance(Simhash(['how', 'owa', 'war', 'are', 'reu', 'eui', 'uia', 'iam', 'amf', 'mfi', 'fin', 'ine', 'net', 'eth', 'tha', 'han', 'ank', 'nks']
# )))


import re
from simhash import Simhash, SimhashIndex
def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

data = {
    "key1": u'How are you? I Am fine. blar blar blar blar blar Thanks.',
    "key2": u'How are you i am fine. blar blar blar blar blar than',
    "key3": u'This is simhash test.',
}
objs = [(str(k), Simhash(get_features(v))) for k, v in data.items()]
print(objs)
index = SimhashIndex(objs, k=4)#k相当于海明距离

print(index.bucket_size())

s1 = Simhash(get_features(u'How are you i am fine. blar blar blar blar blar thank'))
print(index.get_near_dups(s1))

index.add('4', s1)
print(index.get_near_dups(s1))

#二进制位的比对 只能在内存中进行
#  序列化工具：将一个对象转换为二进制
#  反序列化：二进制--＞对象