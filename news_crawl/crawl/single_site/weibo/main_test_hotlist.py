__author__ = 'Administrator'

from single_site.weibo import wb_crawler

#实时热搜榜
weibo = wb_crawler.get_hotlist_weibo('realtimehot')
print(weibo)

#热点热搜榜
weibo = wb_crawler.get_hotlist_weibo('total')
print(weibo)

#潮流热搜榜
weibo = wb_crawler.get_hotlist_weibo('total&key=films')
print(weibo)

#名人热搜榜
weibo = wb_crawler.get_hotlist_weibo('total&key=person')
print(weibo)