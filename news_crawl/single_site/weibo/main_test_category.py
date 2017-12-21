__author__ = 'Administrator'

from single_site.weibo import wb_crawler


#头条
webbos = wb_crawler.get_category_weibo('1760', start_page=1, max_page=3)
print(webbos)


#热门
webbos = wb_crawler.get_category_weibo('0', start_page=1, max_page=3)
print(webbos)

#明星
webbos = wb_crawler.get_category_weibo('2', start_page=1, max_page=3)
print(webbos)

#社会
webbos = wb_crawler.get_category_weibo('7', start_page=1, max_page=3)
print(webbos)

#军事
webbos = wb_crawler.get_category_weibo('4', start_page=1, max_page=3)
print(webbos)

#美女
webbos = wb_crawler.get_category_weibo('10007', start_page=1, max_page=3)
print(webbos)

#体育
webbos = wb_crawler.get_category_weibo('3', start_page=1, max_page=3)
print(webbos)