#构建一个请求对象

class Request(object):
    def __init__(self,url,method = "GET",query={},body={}):
        self.url = url
        self.method = method
        if not isinstance(query,dict):
            raise TypeError("query must be dict")
        self.query = query

        if not isinstance(body, dict):
            raise TypeError("body must be dict")
        self.body = body
