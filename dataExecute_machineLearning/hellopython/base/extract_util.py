__author__ = 'Administrator'

import re


def extract_num_one(str):
    SEARCH_PAT = re.compile(r'(\d+)')
    pat_search = SEARCH_PAT.search(str)
    if pat_search != None:
        return pat_search.group(0)



if __name__ == '__main__':
    print(extract_num_one('a'))

