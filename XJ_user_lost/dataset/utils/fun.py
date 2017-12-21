import importlib
import log
import logging
import os
import utils.constants as constants

logger = logging.getLogger(__name__)
def myfun():
    logger.info('myfun: This is an info message')
    logger.error('myfun: This is an ERROR messages')


"""
Convert the indexes count map to a labels count map.
For example:
the indexes map is:
    {
        0 : 5000,
        1 : 1000,
        2 : 2000
    }
and the labels index map is:
    {
        'train' : 0,
        'val'   : 1,
        'test'  : 2
    }
then the converted result is:
    {
        'train' : 5000,
        'val'   : 1000,
        'test'  : 2000
    }

If the labels_index is empty, return indexes_count directly.
"""
def _indexes_2_labels_count(indexes_count, labels_index):
    logger.info('Convert the indexes count map to a labels count map.')
    labels_count = None
    if len(labels_index) == 0:
        labels_count = indexes_count
    else:
        labels_count = {}
        for key, value in labels_index.items():
            labels_count[key] = indexes_count[value]
    return labels_count


"""
Convert the labels map in format: 
    {
        label1 : n1,
        label2 : n2,
        ...,
        labeln : nn
    }
to a string in format:
    label1 : n1, label2 : n2, ..., labeln : nn
If the map is empty, return a string of None.
"""
def _labels_map_2_string(map):
    logger.info('Convert the labels map to string.')
    string = 'None'
    if len(map) > 0:
        # trim {}
        string = str(map)[1:-1]
    return string


"""
Using 'framework_name'.count_labels function to count labels of all 
records under the dataset directory, then save the result to 
labels_count.txt under the dataset directory
In format:
    <BOF>
    train labels count string
    val labels count string
    test labels count string
    <EOF>
    e.g.: 
    label1 : n1, label2 : n2, ..., labeln : nn
    label1 : n1, label2 : n2, ..., labeln : nn
    label1 : n1, label2 : n2, ..., labeln : nn
        or
    label1 : n1, label2 : n2, ..., labeln : nn
    None
    label1 : n1, label2 : n2, ..., labeln : nn
        or
    ...
"""
def save_labels_count(module_name, dataset_dir):
    cnt_filename = dataset_dir + '/' + constants.LABELS_COUNT_FILE
    logger.info('Save all labels count to "%s"' % cnt_filename)

    labels_idx = {}
    idx_filename = dataset_dir + '/' + constants.LABELS_INDEX_FILE
    if os.path.exists(idx_filename):
        idx_file = open(idx_filename, 'r')
        try:
            for line in idx_file:
                label, index = line.split(' ')
                labels_idx[label] = int(index)
        finally:
            idx_file.close()

    train_db = '%s/%s' % (dataset_dir, constants.TRAIN_DB)
    val_db   = '%s/%s' % (dataset_dir, constants.VAL_DB)
    test_db  = '%s/%s' % (dataset_dir, constants.TEST_DB)
    module = importlib.import_module(module_name)
    # 
    # count_indexes() function should be defined in the module
    #
    count_indexes = getattr(module, "count_indexes")
    train_indexes_count = count_indexes(train_db)
    train_labels_count = _indexes_2_labels_count(train_indexes_count, labels_idx)
    val_indexes_count = count_indexes(val_db)
    val_labels_count = _indexes_2_labels_count(val_indexes_count, labels_idx)
    test_indexes_count = count_indexes(test_db)
    test_labels_count = _indexes_2_labels_count(test_indexes_count, labels_idx)

    train_string = _labels_map_2_string(train_labels_count)
    val_string   = _labels_map_2_string(val_labels_count)
    test_string  = _labels_map_2_string(test_labels_count)
    logger.info('Labels count of train is: %s' % train_string)
    logger.info('Labels count of validation is: %s' % val_string)
    logger.info('Labels count of test is: %s' % test_string)
    cnt_file = open(cnt_filename, 'w')
    try:
        cnt_file.write(train_string)
        cnt_file.write('\n')
        cnt_file.write(val_string)
        cnt_file.write('\n')
        cnt_file.write(test_string)
    finally:
        cnt_file.close()

