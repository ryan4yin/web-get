# -*- coding:utf-8 -*-


import unittest
from pprint import pprint

from utils import *
from bilibili import BilibiliDownloader


class TestData:
    test_av = [
        {
            'url': "https://www.bilibili.com/video/av11297636",
            'page-1': {'cid': 18683622,
                       'duration': 1103,
                       'from': 'vupload',
                       'page': 1,
                       'part': '00.陈涛笛子教学 序讲 Teaching Flute by Chen Tao',
                       'vid': '',
                       'weblink': ''},
            'page-num': 17,
            'info-page-1': {'accept_description': ['高清 1080P', '高清 720P', '清晰 480P', '流畅 360P'],
                            'accept_format': 'flv,hdmp4,flv480,mp4',
                            'accept_quality': [80, 48, 32, 16],
                            # 'durl': [],  # durl 每次请求都会有不同的结果
                            'format': 'flv',
                            'from': 'local',
                            'quality': 80,
                            'result': 'suee',
                            'seek_param': 'start',
                            'seek_type': 'offset',
                            'timelength': 1102514,
                            'video_codecid': 7}
        },
    ]


def get_downloader(url):
    """获取downloader对象
    如果已经缓存了，就直接读取。(开发阶段用缓存的话，就不会一不小心被封ip了)
    否则就新建"""

    dump_name = url.rsplit('/')[-1] + '.pickle'
    dump_path = './pickles/' + dump_name

    if has_file('./pickles', dump_name):
        downloader = load(dump_path)
    else:
        downloader = BilibiliDownloader(url)
        dump(downloader, dump_path)

    return downloader


class TestBilibiliDowloader(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_av(self):
        for item in TestData.test_av:
            downloader = get_downloader(item['url'])
            parser = downloader.parser
            pages = parser.get_av_pages()  # 测试parser

            # 确定parser工作正常
            self.assertEqual(len(pages), item['page-num'])
            self.assertEqual(pages[0], item['page-1'])

            # 确定 get_video_info 工作正常
            info = downloader.get_video_info(pages[0]['cid'], 116)  # 116 最高的清晰度参数
            info.pop('durl')   # durl 每次请求都会有不同的结果
            self.assertEqual(info, item['info-page-1'])






