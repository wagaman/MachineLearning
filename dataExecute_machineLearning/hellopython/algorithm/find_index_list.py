__author__ = 'sss'


if __name__ == '__main__':

    item_list = [(1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1)]

    test_score = 3.5
    index_close = None
    for index in range(0, len(item_list) - 1):
        item = item_list[index]
        item_next = item_list[index + 1]
        if item_next[1] < test_score < item[1]:
            index_close = index
            break

    print(index_close)