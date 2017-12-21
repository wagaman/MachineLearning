__author__ = 'Administrator'

from single_site.zhihu import zh_crawler

with open('search_list.txt', 'a', encoding='utf8') as f:
    search_word = '苍井空'  # 互联网话题ID
    answers = zh_crawler.get_search_list(search_word, f, start_page=1, max_page=3)
    print(answers)