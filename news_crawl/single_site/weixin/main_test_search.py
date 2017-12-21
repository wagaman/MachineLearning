__author__ = 'Administrator'

from single_site.weixin import wx_crawler

#抓取公众号   json解析错误，要用selenium
media_url = 'http://mp.weixin.qq.com/profile?src=3&timestamp=1498199407&ver=1&signature=La95QBhbfRQECzxLVQJJA-7osPzuOrSRVznNOZ-9jlwIoD6I5o5hXvsieGgSQwxHuVyDRv3bv5a89JDuTGbdzQ=='
chapters = wx_crawler.get_media_by_url(media_url)
print(chapters)


#搜索公众号  最多10页
medias = wx_crawler.get_search_media_weixin('你', start_page=0, max_page=2)
print(medias)

#抓取文章  北京暴雨去哪了
chapter_url = 'http://mp.weixin.qq.com/s?src=3&timestamp=1498198805&ver=1&signature=vpRcnDWL4y-O1NScjqfxBhgwSnJGMIjv1sdNvkDUCNZl1n8yQQRekp-FEpCZFtK1P9ft8RRh9APNsJ1vU1Mf*gggohXrMibTqU1Ilqeg2wlN8SLHjZvw7skVk207*ltaR3an*bvikSELeAOKknZjTR2le5TlwsI9z4Z0WrcwDNY='
chapter = wx_crawler.get_chapter_by_url(chapter_url)
print(chapter)


#搜索文章  最多10页
chapters = wx_crawler.get_search_chapter_weixin('北京暴雨', start_page=0, max_page=3)
print(chapters)











