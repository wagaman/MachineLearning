__author__ = 'Administrator'

from single_site.zhihu_sougou import zhihu_crawler

category = {}
category['今日最热'] = 'hot/hot'
category['编辑推荐'] = 'recommend/recommend'
category['运动'] = 'topic/topic1_'
category['互联网'] = 'topic/topic2_'
category['艺术'] = 'topic/topic3_'
category['阅读'] = 'topic/topic4_'
category['美食'] = 'topic/topic5_'
category['动漫'] = 'topic/topic6_'
category['汽车'] = 'topic/topic7_'
category['生活方式'] = 'topic/topic8_'
category['教育'] = 'topic/topic9_'
category['摄影'] = 'topic/topic10_'
category['历史'] = 'topic/topic11_'
category['文化'] = 'topic/topic12_'
category['旅行'] = 'topic/topic12_'
category['职业发展'] = 'topic/topic13_'
category['经济学'] = 'topic/topic14_'
category['足球'] = 'topic/topic15_'
category['篮球'] = 'topic/topic16_'
category['投资'] = 'topic/topic17_'
category['音乐'] = 'topic/topic18_'
category['电影'] = 'topic/topic19_'
category['法律'] = 'topic/topic20_'
category['自然科学'] = 'topic/topic21_'
category['设计'] = 'topic/topic22_'
category['创业'] = 'topic/topic23_'
category['健康'] = 'topic/topic24_'
category['商业'] = 'topic/topic25_'
category['体育'] = 'topic/topic26_'
category['科技'] = 'topic/topic27_'
category['化学'] = 'topic/topic28_'
category['物理学'] = 'topic/topic29_'
category['生物学'] = 'topic/topic30_'
category['金融'] = 'topic/topic31_'



#今日最热
zhihus = zhihu_crawler.get_category_zhihu(category, start_page=0, max_page=2, type='汽车')
print(zhihus)








