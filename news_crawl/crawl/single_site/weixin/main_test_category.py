__author__ = 'Administrator'

from single_site.weixin import wx_crawler

category = {}
category['热门'] = 'pc_0'
category['推荐'] = 'pc_1'
category['段子手'] = 'pc_2'
category['养生堂'] = 'pc_3'
category['私房活'] = 'pc_4'
category['八卦精'] = 'pc_5'
category['爱生活'] = 'pc_6'
category['财经迷'] = 'pc_7'
category['汽车迷'] = 'pc_8'
category['科技咖'] = 'pc_9'
category['潮人帮'] = 'pc_10'
category['辣妈帮'] = 'pc_11'
category['点赞党'] = 'pc_12'
category['旅行家'] = 'pc_13'
category['职场人'] = 'pc_14'
category['美食家'] = 'pc_15'
category['古今通'] = 'pc_16'
category['学霸族'] = 'pc_17'
category['星座控'] = 'pc_18'
category['体育迷'] = 'pc_19'

#热门
weixins = wx_crawler.get_category_weixin('pc_0', start_page=0, max_page=1)
print(weixins)

#推荐
weixins = wx_crawler.get_category_weixin('pc_1', start_page=0, max_page=1)
print(weixins)

#段子手
weixins = wx_crawler.get_category_weixin('pc_2', start_page=0, max_page=1)
print(weixins)


