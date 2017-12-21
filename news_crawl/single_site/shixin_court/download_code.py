import uuid
import requests

__author__ = 'sss'

defalut_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
    "Host": "shixin.court.gov.cn",
    "Origin": "http://shixin.court.gov.cn",

    "Cookie": "_gscs_2025930969=09928799rtb5tx11|pv:1; _gscbrs_2025930969=1; JSESSIONID=406D94C0EABD377CA529B94285D5BC9E; _gscu_2025930969=09618250ualvq911",

    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

for i in range(100):
    uuid_tmp = uuid.uuid4().__str__().replace('-', '')
    url = 'http://shixin.court.gov.cn/captchaNew.do?captchaId=' + uuid_tmp

    filename = 'C:\\Users\sss\Downloads\验证码\shixin_count\\' + uuid_tmp +'.jpg'

    ir = requests.get(url, headers=defalut_headers)
    if ir.status_code == 200:
        open(filename, 'wb').write(ir.content)