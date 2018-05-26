# -*- coding:utf-8 -*-

"""
不登录，直接从给出的bilibili链接中获取流视频

P.S. B站以前曾经使用过好几种链接，这里就只解析现在使用的这种了。
用浏览器访问时，旧链接会被重定向到新链接。可以获取新链接再下载。
"""

import re


class Bilibili:
    _APP_KEY = '84956560bc028eb7'
    _BILIBILI_KEY = '94aba54af9065f71de72f5508f1cd42e'
    
    # 基础链接的正则
    regex_bangumi_list = r"https?://www\.bilibili\.(?:tv|com)/bangumi/media/md(\d+)"
    regex_bangumi = r"https?://www\.bilibili\.(?:tv|com)/bangumi/play/ep(\d+)"

    regex_av = r"https?://www\.bilibili\.(?:tv|com)/video/av(\d+)/?p=(\d+)"

    def type_detect(self, url):
        pass





