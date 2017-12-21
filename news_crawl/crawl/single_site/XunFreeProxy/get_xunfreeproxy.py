# /usr/bin/python
# encoding:utf-8

'''
获取免费的讯代理 http://www.xdaili.cn/freeproxy.html
'''

import requests
import json

xun_free_url = "http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10"

xun_proxy_list = []
proxies = {}


def get_xun_free_proxy():
	try:
		global xun_proxy_list
		response = requests.get(xun_free_url)
		xun_proxy_list_result = []
		for x in range(len(response.json()["rows"])):
			xun_proxy = response.json()["rows"][x]["ip"] + ":" + response.json()["rows"][x]["port"]
			xun_proxy_list_result.append(xun_proxy)
		xun_proxy_list = xun_proxy_list + xun_proxy_list_result
		return xun_proxy_list
	except Exception as e:
		print(e)
	finally:
		pass


def get_one_from_list():
	try:
		global xun_proxy_list
		del xun_proxy_list[0]
		if len(xun_proxy_list) <= 5:
			get_xun_free_proxy()
		return xun_proxy_list[0]
	except Exception as e:
		print(e)
	finally:
		pass

get_xun_free_proxy()



