# -*- coding: utf-8 -*-
import scrapy, json, time, re


class ArtilcSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['qq.com']
    start_urls = ['http://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzU3NjE3Mzg2Mg==&f=json&offset=0&count=10&is_ok=1&scene=&uin=MTk3NjM1NTkyMQ%3D%3D&key=467d76de74d244698e5c0e82f216615f2cc80f907e6606a90f507a72149eac2a752dc830763caf759ae2df5593f3a6cdcdd1a42fecd95f5028af03611cb71c4b10cdfab042ad84942f29a73a44faa963&pass_ticket=lK5zHDOEPl8xpjD%2F8e8rZkYAX1Y%2F7tIkTp%2B2KJwSvQh0HysVnoSTi8EEEgo854Jl&wxtoken=&appmsg_token=959_Rsmpt8t2mZv4CN3cYhhi4KdfJQQYqgbXCRi1Pg~~&x5=0&f=json']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1976355921; devicetype=Windows10; version=6206021f; lang=zh_CN; pass_ticket=lK5zHDOEPl8xpjD/8e8rZkYAX1Y/7tIkTp+2KJwSvQh0HysVnoSTi8EEEgo854Jl; wap_sid2=CNGYs64HElxZRTFVdzkzbHVBTGY3cDFybnRHR2lULWFIak9hcHRYUktWVXoyNmFfVVpuTGQxckozWkstTHpvV0F3U1JCZlMxd2NTLVVaRHdSdTFNaW9OWnk0Q0pLNzhEQUFBfjDByL7YBTgNQJVO',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzU3NjE3Mzg2Mg==&uin=MTk3NjM1NTkyMQ%3D%3D&key=467d76de74d244698e5c0e82f216615f2cc80f907e6606a90f507a72149eac2a752dc830763caf759ae2df5593f3a6cdcdd1a42fecd95f5028af03611cb71c4b10cdfab042ad84942f29a73a44faa963&devicetype=Windows+10&version=6206021f&lang=zh_CN&a8scene=7&pass_ticket=lK5zHDOEPl8xpjD%2F8e8rZkYAX1Y%2F7tIkTp%2B2KJwSvQh0HysVnoSTi8EEEgo854Jl&winzoom=1',
        }
    }
    def parse(self, response):
        yield scrapy.Request(
            url=response.url,
            callback=self.parse_all_page,
            dont_filter=True,
            meta={
                'offset': 0,
            }
        )

    def parse_all_page(self, response):
        offset = response.meta['offset']
        root = response.text
        result = json.loads(root)
        if not result['errmsg'] == 'ok':
            print('没有文章了')
        else:
            info = result['general_msg_list']
            result2 = json.loads(info)
            for article in result2['list']:
                article_title = article['app_msg_ext_info']['title']
                article_title = article_title.replace(",", "，")
                article_datetime = article['comm_msg_info']['datetime']
                article_datetime = int(article_datetime)
                article_datetime = time.localtime(article_datetime)
                # 转换成新的时间格式(2016-05-05 20:28:54)
                article_datetime = time.strftime("%Y-%m-%d", article_datetime)
                article_img_src = article['app_msg_ext_info']['cover']
                print(article_title, article_datetime)
                with open('article.csv', 'a') as f:
                    f.write(article_title+","+article_datetime+','+article_img_src+'\n')
            url = self.start_urls[0]
            pattern = re.compile(r'offset=(\d+)')
            url = pattern.sub('offset={}'.format(offset+10), url)
            yield scrapy.Request(
                url=url,
                callback=self.parse_all_page,
                dont_filter=True,
                meta={
                    'offset': offset+10
                }
            )
