__author__ = 'Administrator'

from single_site.zhihu import zh_crawler

with open('questions_list.txt', 'a', encoding='utf8') as f:
    topic_id = 19550517  # 互联网话题ID
    zh_crawler.get_huati_questions_list(topic_id, f, start_page=1, max_page=10)

