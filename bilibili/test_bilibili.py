# -*- coding:utf-8 -*-


import unittest
from collections import OrderedDict
from pprint import pprint

from utils import *
from bilibili import Bilibili


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
            'video-page-1': {'accept_description': ['高清 1080P', '高清 720P', '清晰 480P', '流畅 360P'],
                             'accept_format': 'flv,hdmp4,flv480,mp4',
                             'accept_quality': [80, 48, 32, 16],
                             # 'durl': [],  # durl 每次请求都可能会有不同的结果
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

    test_bangumi_ep = [
        {
            'url': "https://www.bilibili.com/bangumi/play/ep199959",
            'video': {'accept_format': 'hdflv2,flv,flv720,flv480,flv360',
                      'accept_quality': '112,80,64,32,15',
                      # 'durl': [],  # durl 每次请求都可能会有不同的结果
                      'bp': '0',
                      'format': 'flv480',
                      'from': 'local',
                      'has_paid': 'false',
                      'quality': '32',
                      'result': 'suee',
                      'seek_param': 'start',
                      'seek_type': 'offset',
                      'status': '2',
                      'timelength': '1374376',
                      'vip_status': '0',
                      'vip_type': '0'}

        },
    ]

    test_bangumi_list = [
        {
            'url': "https://www.bilibili.com/bangumi/media/md78512",
            'video': {'accept_format': 'hdflv2,flv,flv720,flv480,flv360',
                      'accept_quality': '112,80,64,32,15',
                      'bp': '0',
                      # 'durl': [],   # durl 每次请求都会有不同的结果
                      'format': 'flv480',
                      'from': 'local',
                      'has_paid': 'false',
                      'quality': '32',
                      'result': 'suee',
                      'seek_param': 'start',
                      'seek_type': 'offset',
                      'status': '2',
                      'timelength': '1374376',
                      'vip_status': '0',
                      'vip_type': '0'
                      },
        },
    ]


def get_bilibili_parser(url):
    """获取downloader对象
    如果已经缓存了，就直接读取。(开发阶段用缓存的话，就不会一不小心被封ip了)
    否则就新建"""

    dump_name = url.rsplit('/')[-1] + '.pickle'
    dump_path = './pickles/' + dump_name

    if has_file('./pickles', dump_name):
        bilibili_parser = load(dump_path)
    else:
        bilibili_parser = Bilibili(url)
        dump(bilibili_parser, dump_path)

    return bilibili_parser


class TestBilibili(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_av(self):
        for item in TestData.test_av:
            bilibili_parser = get_bilibili_parser(item['url'])
            av_parser = bilibili_parser._parser
            pages = av_parser.get_av_pages()  # 测试parser

            # 确定parser工作正常
            self.assertEqual(len(pages), item['page-num'])
            self.assertEqual(pages[0], item['page-1'])

            # 确定 get_video_info 工作正常
            video_info = bilibili_parser._get_av_info(pages[0]['cid'], 112)  # 112 最高的清晰度参数(116收费可用)
            video_info.pop('durl')  # durl 每次请求都会有不同的结果
            self.assertEqual(video_info, item['video-page-1'])

    def test_bangumi_ep(self):
        for item in TestData.test_bangumi_ep:
            bilibili_parser = get_bilibili_parser(item['url'])
            ep_parser = bilibili_parser._parser

            # 测试ep
            ep = ep_parser.get_epinfo()

            # 拿下载链接
            video_info = bilibili_parser._get_bangumi_info(ep['cid'], 112)
            video_info.pop('durl')  # durl 每次请求都会有不同的结果

            self.assertEqual(video_info, item['video'])
