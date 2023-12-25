FROM my-python:3.8.3
RUN pip install --default-timeout=120 requests pymysql redis aiohttp tornado selenium appium-python-client

# 安装gcc编译环境和其他依赖
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev libxml2-dev libxslt-dev zlib1g-dev libffi-dev libssl-dev libcurl4-openssl-dev \
    && pip --default-timeout=120 install twisted gevent scrapy pyspider \
    && rm -rf /var/lib/apt/lists/*

RUN pip install websocket-client
RUN pip install sqlalchemy
RUN pip install simhash