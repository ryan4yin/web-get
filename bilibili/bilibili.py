# -*- coding:utf-8 -*-

"""
不登录，直接从给出的bilibili链接中获取流视频

P.S. B站以前曾经使用过好几种链接，这里就只解析现在使用的这种了。（eg. ` bangumi.bilibili.com` `bilibili.tv`)
用浏览器访问时，旧链接会被重定向到新链接。可以获取新链接再下载。
"""
import hashlib
import re
import json
from urllib import parse

import requests

import logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# 复制自 chrome
user_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}

# b站的验证措施，需要用到这几个固定参数
_APP_KEY = '84956560bc028eb7'
_BILIBILI_KEY = '94aba54af9065f71de72f5508f1cd42e'    # for av
_BILIBILI_KEY_2 = '9b288147e5474dd2aa67085f716c560d'  # for bangumi

# 视频清晰度, 复制自bilibili-helper
QUALITY_DISPLAY_NAMES = {
    116: '2k?',
    112: '1080P+',
    80: '1080P',
    64: '720P',
    48: '720P',
    32: '480P',
    16: '360P',
}

api_url = 'http://interface.bilibili.com/v2/playurl'
bangumi_api_url = 'http://bangumi.bilibili.com/player/web_api/playurl'


class BilibiliDownloader:
    """主类"""
    # 1. 动漫播放页
    regex_ep = re.compile(r"(?P<url>https?://www\.bilibili\.com/bangumi/play/ep(?P<ep>\d+))")

    # 2. 动漫首页
    regex_home = re.compile(r"(?P<url>https?://www\.bilibili\.com/bangumi/media/md(?P<md>\d+))")

    # 3. av播放页
    regex_p = re.compile(r"(?P<url>https?://www\.bilibili\.com/video/av(?P<avid>\d+)(?:/\?p=(?P<pname>\d+)|))")

    def __init__(self, url):
        # 首先检测url是否符合要求，并提取出需要的信息
        url_type, self.args = self.type_check(url)

        self.__session = requests.Session()
        self.__text = self.__session.get(url=self.args['url'], headers=user_agent).text  # 拿到给定网页

        self.parser = self.get_parser(url_type)

    def type_check(self, url):
        """use match，not fullmatch"""
        match = self.regex_ep.match(url)  # 1. 是动漫的播放页？
        if match:
            return 'bangumi', match.groupdict()

        match = self.regex_home.match(url)  # 2. 是动漫的主页？
        if match:
            return 'bangumi_home', match.groupdict()

        match = self.regex_p.match(url)  # 3. 是up主上传的视频？
        if match:
            return 'av', match.groupdict()

        # 否则，就是不支持的链接。
        raise RuntimeError("The given link is not supported.")

    def get_parser(self, url_type):
        if url_type == 'bangumi':
            return BangumiEpParser(self.__text)
        elif url_type == 'bangumi_home':
            return BangumiHomeParser(self.__text)
        elif url_type == 'av':
            return AvParser(self.__text)
        else:
            raise RuntimeError("url_type不可能为其他参数，请检查代码。")

    def get_video_info(self, cid, quality):
        """通过 interface.bilibili.com 的 api 获取视频源地址。"""
        params = {
            'appkey': _APP_KEY,
            'cid': cid,
            'otype': 'json',
            'qn': quality,
            'quality': quality,  # 这俩相同的参数指定视频质量
            'type': '',  # 这个指定是flv还是mp4
        }
        params_str = parse.urlencode(params, encoding='utf-8')
        sign = hashlib.md5(bytes(params_str + _BILIBILI_KEY, 'utf8')).hexdigest()  # 签名这一步，需要用到 _BILIBILI_KEY
        params.update({'sign': sign})

        headers = {
            'refer': self.args['url'],
        }
        headers.update(user_agent)

        resp = requests.get(url=api_url, params=params, headers=headers)

        return resp.json()


class AvParser:
    """av页面解析器（此av非彼av。。）"""

    # 匹配此av的pages，json格式（位置：网页源代码）
    regex_pages = re.compile(r'"pages":(\[[^\]]*\])')

    def __init__(self, text):
        self.text = text  # 网页内容

    def get_av_pages(self):
        """获取av的pages列表，几个Parser的get方法代码高度重复。"""
        match = self.regex_pages.search(self.text)
        json_str = match.group(1)
        return json.loads(json_str)


class BangumiEpParser:
    """动漫播放页解析器"""

    # 本p的信息，json格式（位置：网页源代码）
    regex_epinfo = re.compile(r'"epInfo":({[^}]*})')
    # 此动漫的episodes，json格式（位置：网页源代码）
    regex_epList = re.compile(r'"epList":(\[[^\]]*\])')

    def __init__(self, text):
        self.text = text

    def get_epinfo(self):
        match = self.regex_epinfo.search(self.text)
        json_str = match.group(1)
        return json.loads(json_str)

    def get_epList(self):
        match = self.regex_epList.search(self.text)
        json_str = match.group(1)
        return json.loads(json_str)


class BangumiHomeParser:
    """动漫首页解析器"""

    # 和 BangumiEP 中的epList一模一样的内容，只是名字不同。
    regex_episodes = re.compile(r'"episodes":(\[[^\]]*\])')

    def __init__(self, text):
        self.text = text

    def get_episodes(self):
        match = self.regex_episodes.search(self.text)
        json_str = match.group(1)
        return json.loads(json_str)
