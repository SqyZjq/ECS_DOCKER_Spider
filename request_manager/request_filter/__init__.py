import urllib.parse

class RequestFilter(object):
    def __init__(self, filter_obj):
        """
        初始化请求去重的对象
        """
        self.filter_obj = filter_obj

    def is_exists(self, request_obj):
        """
        判断请求是否已经处理过
        :param request_obj: 请求对象
        :return: True 如果请求已存在，否则 False
        """
        data = self._get_request_filter_data(request_obj)
        return self.filter_obj.is_exists(data)

    def mark_request(self, request_obj):
        """
        标记已经处理的请求对象
        :param request_obj: 请求对象
        :return: 无返回值
        """
        data = self._get_request_filter_data(request_obj)
        self.filter_obj.save(data)

    def _get_request_filter_data(self, request_obj):
        """
        根据请求对象，处理其数据，转换为字符串后用于去重
        :param request_obj: 请求对象
        :return: 转换后的字符串
        """
        url = request_obj.url
        parsed_url = urllib.parse.urlparse(url)
        # 统一协议和域名为小写，其他保留原始格式
        url_without_query = parsed_url.scheme.lower() + "://" + parsed_url.hostname.lower() + parsed_url.path
        # 解析 URL 中的查询参数
        url_query = urllib.parse.parse_qsl(parsed_url.query)
        # 请求方法转大写
        method = request_obj.method.upper()
        # 如果 request_obj 有 query 属性，则获取其 items，否则为空列表
        query = request_obj.query.items() if hasattr(request_obj, 'query') else []
        # 将 URL 查询参数和 request_obj 的查询参数合并后排序
        all_query = sorted(list(query) + url_query, key=lambda kv: kv[0])
        print(all_query)
        # 重构含有查询参数的 URL
        url_with_query = url_without_query + "?" + urllib.parse.urlencode(all_query)
        # 如果 request_obj 有 body 属性，则获取其 items 并排序转为字符串，否则为空字符串
        str_body = str(sorted(request_obj.body.items())) if hasattr(request_obj, 'body') else ''
        # 将 URL、请求方法和 body 组合成最终的字符串
        data = url_with_query + method + str_body
        return data
