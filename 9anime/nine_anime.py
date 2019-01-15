# -*- coding:utf-8 -*-

"""
通过网页地址，下载 www59anime.is 的在线动漫
"""

import requests

resp = requests.get("http://www.baidu.com")
req = resp.request
print(req.headers, req.body)

