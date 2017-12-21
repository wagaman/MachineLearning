__author__ = 'Administrator'
from single_site.XunFreeProxy import get_xunfreeproxy
import requests
defalut_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
    "Host": "weixin.sogou.com",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",

    "X-Requested-With": "XMLHttpRequest"
}

params = {'query': '你好',
          '_sug_type_': 1,
          'sut': 0,
          'type': '2',
          'ie': 'utf8',
          'ri': 0,
          'page': 1}
url = 'http://www.baidu.ml'
proxies = {"http": "http://" + get_xunfreeproxy.get_one_from_list()}
response = requests.get(url, proxies=proxies, timeout=60)
print(response.text)