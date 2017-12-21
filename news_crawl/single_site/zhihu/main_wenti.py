__author__ = 'Administrator'

from single_site.zhihu import zh_crawler

question_id = 19794858
q = zh_crawler.get_question(question_id)
print(q)
