import uuid
import requests

__author__ = 'sss'

defalut_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
    "Host": "shixin.csrc.gov.cn",

    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

for i in range(100):
    uuid_tmp = uuid.uuid4().__str__().replace('-', '')
    url = 'http://shixin.csrc.gov.cn/honestypub/login/ycode.do'

    filename = 'C:\\Users\sss\Downloads\验证码\csrc_gov\\' + uuid_tmp +'.jpg'

    ir = requests.get(url, headers=defalut_headers)
    if ir.status_code == 200:
        open(filename, 'wb').write(ir.content)