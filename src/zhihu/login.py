# -*- coding:utf-8 -*-

"""
使用 requests, 模拟登录知乎.

Author: ryan yin
"""

import requests
from time import time
import execjs


class ZhihuSession:
    # 0. home 主页网址
    home_url = 'https://www.zhihu.com/'

    # 1. User-Agent 复制自 Chrome 请求
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"

    # 2. 登录页面
    login_url = 'https://www.zhihu.com/signup?nex=%2F'

    # 3. 登录接口
    login_api = 'https://www.zhihu.com/api/v3/oauth/sign_in'

    # 获取验证码的url
    capture_url = "https://www.zhihu.com/api/v3/oauth/captcha?lang=en"

    # 分析网站发现这是一个固定值。
    client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'

    main_header = {
        'Host': 'www.zhihu.com',
        'user-agent': user_agent,
    }

    def __init__(self, user_name=None, passwd=None, cookies=None):
        """

        :param user_name: 用户名
        :param passwd: 密码
        :param cookie: 如果提供了cookie，就通过cookie登录
        """
        self.session = requests.Session()  # 创建会话

        self.user_name = user_name
        self.passwd = passwd
        self.cookies = cookies

    def login(self):
        """
        需要先访问特定的几个网址，
        这几个访问的 response 会设置必要的 cookie (通过 set-cookie 首部)
        :return:
        """
        headers = self.main_header.copy()
        headers.update({
            'referer': self.login_url,
            'authorization': 'oauth ' + self.client_id,
        })

        # 1. get 请求登录页面，会设置四个 cookie: tgw_l7_route  _xsrf  d_c0  q_c1
        self.session.get(self.login_url, headers=headers)

        # 2. 然后会请求几个js，其中会设置 x-udid, 不过这个参数没有也没问题？

        # 3. 会访问两次 capture，刚进去是注册页面，会访问一次capture, 然后点击进入登录页面，也会访问一次。
        # 这两次访问会设置 cookie：capsion_ticket, 运气不好还会有验证码
        self.session.get(url=self.capture_url, headers=headers)
        self.session.get(url=self.capture_url, headers=headers)

        # 4. 登录，这一步，请求头会多一个 x-xsrftoken，也是js设置的，不知道不设会不会有问题
        headers.update({'origin': 'https://www.zhihu.com'})

        time_stamp = Utils.get_timestamp()  # 时间戳，单位毫秒

        with open('./getSignature.js', 'r') as f:
            ctx = execjs.compile(f.read())
            signature = ctx.call('getSignature', time_stamp)  # 计算出 signature

        form_data = {
            'client_id': self.client_id,
            'grant_type': 'password',
            'timestamp': str(time_stamp),
            'source': "com.zhihu.web",
            'signature': signature,
            'username': self.user_name,
            'password': self.passwd,
            'capture': '',
            'lang': 'en',
            'ref_source': 'other',
            'utm_source': ''
        }

        return self.session.post(url=self.login_api, headers=headers, data=form_data)

    def check_login(self):
        headers = self.main_header.copy()
        headers.update({
            'Referer': 'https://www.zhihu.com/',
        })

        if self.cookies:
            return self.session.get(url=self.home_url, headers=headers, cookies=self.cookies)
        else:
            return self.session.get(url=self.home_url, headers=headers)


class Utils:
    @staticmethod
    def get_timestamp():
        return int(time() * 1000)


if __name__ == "__main__":
    session = ZhihuSession(user_name='你的账号', passwd='你的密码')

    print(session.login())
    resp = session.check_login()
