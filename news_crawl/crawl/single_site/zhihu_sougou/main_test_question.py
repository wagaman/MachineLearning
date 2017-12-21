__author__ = 'Administrator'

from single_site.zhihu_sougou import zhihu_crawler

question_id = 19794858
zhihus = zhihu_crawler.get_question_json(question_id)
print(zhihus)








