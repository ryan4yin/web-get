# 下载器

想要通过这个项目学会的技能：
- 下载网上能够在线看到，却没有提供下载链接的资料。比如网易/虾米/QQ的音乐、Youtube/Bilibili的视频，百度云的资料等。
- 爬资料做数据分析，比如分析知乎、B站。（这方面会导致大量的请求，因此尤其需要注意爬取策略。）

主流的数据产出网站或者视频网站，像知乎、B站、Youtube、百度云，都应用了反爬虫策略。(因为不反的话，网站要垮。。)
所以并不是拿到直链，随便用个下载器就能下载的。应对方法参见下面的反爬虫的应对。

## 说明

各主流网站的 非开放 api，为了防止被破解或者优化代码，其实是更新得很快的。刚写的代码可能过两三个月就用不了了，这是很正常的事。
因此爬虫其实是很种脆弱的东西，这个项目的代码如果我不时长更新，可能以后就用不了了。
不过万变不离其宗，只要学会了方法和策略，不管网站怎么改，总是能够找到方法的。

## 打算参考的资料

### 模拟登录

如果要下载只有登录用户可见的数据，就需要先模拟登录。
- [python模拟登陆知乎](https://zhuanlan.zhihu.com/p/32898234)
- [ArticleSpider](https://github.com/mtianyan/ArticleSpider)

### 反爬虫的应对

- [常见的反爬虫和应对方法](https://zhuanlan.zhihu.com/p/20520370)
- [PythonSpiderNotes](https://github.com/lining0806/PythonSpiderNotes)

### 视频下载器

- [youtube_dl/extractor/bilibili.py](https://github.com/rg3/youtube-dl/tree/master/youtube_dl/extractor/bilibili.py)
- [you_get/extractors/bilibili.py](https://github.com/soimort/you-get/blob/develop/src/you_get/extractors/bilibili.py)
- [bilibili merged flv+mp4+ass+enhance](https://github.com/liqi0816/bilitwin)

### 库

- [requests](http://docs.python-requests.org/zh_CN/latest/index.html)


