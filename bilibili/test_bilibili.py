# -*- coding:utf-8 -*-


import unittest

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
            'page-len': 17,
            'page-1-info': {'accept_description': ['高清 1080P', '高清 720P', '清晰 480P', '流畅 360P'],
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

    # 要选个更新完结的动画。这个可能会变化
    test_bangumi_ep = [
        {
            'url': "https://www.bilibili.com/bangumi/play/ep15492",
            'title': "丹特丽安的书架",
            'ep': {"aid": 139620,
                   "cid": 232050,
                   "cover": "http:\u002F\u002Fi0.hdslb.com\u002Fbfs\u002Fbangumi"
                            "\u002Ffed869845e441c61b7b2527302647b7250efd787.jpg",
                   "ep_id": 15492,
                   "episode_status": 2,
                   "from": "bangumi",
                   "index": "8",
                   "index_title": "等价之书 & 连理之书",
                   "mid": 72826,
                   "page": 1,
                   "pub_real_time": "2011-09-03 10:21:31",
                   "vid": "60159958"
                   },
            'ep-len': 13,
            'ep-info': {'accept_format': 'flv,flv720,flv360',
                        'accept_quality': '80,64,15',
                        'bp': '0',
                        'format': 'flv360',
                        'from': 'local',
                        'has_paid': 'false',
                        'quality': '15',
                        'result': 'suee',
                        'seek_param': 'start',
                        'seek_type': 'offset',
                        'status': '2',
                        'timelength': '1480369',
                        'vip_status': '0',
                        'vip_type': '0'},

        },
    ]

    test_bangumi_list = [
        {
            'url': "https://www.bilibili.com/bangumi/media/md862",
            'title': "丹特丽安的书架",
            'ep-len': 13,  # 选错了，其实应该选个更新完结的动画。这个可能会变化
            'ep-2-info': {'aid': 115913,
                          'cid': 193520,
                          'cover': 'http://i0.hdslb.com/bfs/bangumi/698c29861265e2ca8f0b80dd3e90ffdd78adf0d5.jpg',
                          'ep_id': 15499,
                          'episode_status': 2,
                          'from': 'bangumi',
                          'index': '1',
                          'index_title': '立体绘本',
                          'mid': 72826,
                          'page': 1,
                          'pub_real_time': '2011-07-16 05:38:24',
                          'vid': '56767980'},
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

            # 1. 测试av_parser
            pages = av_parser.get_av_pages()
            self.assertEqual(len(pages), item['page-len'])
            self.assertEqual(pages[0], item['page-1'])

            # 2. 测试 get_video_info
            video_info = bilibili_parser._get_av_info(pages[0]['cid'], 112)  # 112 最高的清晰度参数
            video_info.pop('durl')  # durl 每次请求都会有不同的结果
            self.assertEqual(video_info, item['page-1-info'])

    def test_bangumi_ep(self):
        for item in TestData.test_bangumi_ep:
            bilibili_parser = get_bilibili_parser(item['url'])
            ep_parser = bilibili_parser._parser

            # 0. 测试获取title
            title = ep_parser.get_title()
            self.assertEqual(title, item['title'])

            # 1. 测试 get_epinfo
            ep = ep_parser.get_epinfo()
            self.assertEqual(ep, item['ep'])

            # 2. 测试 get_epList
            epList = ep_parser.get_epList()
            self.assertEqual(len(epList), item['ep-len'])

            # 测试 get_bangumi_info
            video_info = bilibili_parser._get_bangumi_info(ep['cid'], 80)
            video_info.pop('durl')  # durl 每次请求都会有不同的结果

            self.assertEqual(video_info, item['ep-info'])

    def test_bangumi_home(self):
        for item in TestData.test_bangumi_list:
            bilibili_parser = get_bilibili_parser(item['url'])
            home_parser = bilibili_parser._parser

            # 0. 测试获取title
            title = home_parser.get_title()
            self.assertEqual(title, item['title'])

            # 1. 测试 get_epList
            episodes = home_parser.get_episodes()
            self.assertEqual(len(episodes), item['ep-len'])
            self.assertEqual(item['ep-2-info'], episodes[1])
