__author__ = 'Administrator'

from single_site.zhihu_sougou import zhihu_crawler

zhihus = zhihu_crawler.get_search_zhihu('北京暴雨', start_page=0, max_page=3)
print(zhihus)

#抓取问题







