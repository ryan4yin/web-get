# -*- coding:utf-8 -*-


import unittest

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
            pages = parser.get_av_pages()

            self.assertEqual(len(pages), item['page-num'])
            self.assertEqual(pages[0], item['page-1'])






