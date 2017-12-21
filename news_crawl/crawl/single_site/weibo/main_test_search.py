__author__ = 'Administrator'

from single_site.weibo import wb_crawler

#搜索
weibos, chapters, persions = wb_crawler.get_search_weibo('北京暴雨')
print(weibos)
print(chapters)
print(persions)
