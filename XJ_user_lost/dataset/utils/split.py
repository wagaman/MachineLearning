# -*- coding: utf-8 -*-
import os
import sys
import log
import time
import logging


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import utils.constants
import utils.common as common

logger = logging.getLogger("utils.split")

"""
Create args for parse train folder subprocess
"""
def _create_parse_train_folder_args(args, output_dir, train_image_path, train_file, percent_val, val_file, percent_test, test_file):
    """
    Create args to parse train folder 
    """
    names = []
    names.append('train')
    parse_train_folder_args = []
    labels_file = '%s/labels.txt' % output_dir
    parse_train_folder_args.append(train_image_path)
    parse_train_folder_args.append(labels_file)
    parse_train_folder_args.append('--train_file=%s' % train_file)
    if percent_val:
        names.append('val')
        parse_train_folder_args.append('--val_file=%s' % val_file)
        parse_train_folder_args.append('--percent_val=%s' % percent_val)
    if percent_test:
        names.append('test')
        parse_train_folder_args.append('--test_file=%s' % test_file)
        parse_train_folder_args.append('--percent_test=%s' % percent_test)             

    tmp_parse_folder_args = []
    tmp_parse_folder_args += args
    tmp_parse_folder_args += parse_train_folder_args
    parse_train_folder_args = [str(x) for x in tmp_parse_folder_args]        
    logger.info('Parse Folder (%s) subprocess args: "%s"' % (('/'.join(names), (' '.join(parse_train_folder_args)))))
    print "" 

    return parse_train_folder_args  

"""
Create args for parse val folder subprocess
"""
def _create_parse_val_folder_args(args, output_dir, val_image_path, val_file):  
    parse_val_folder_args = []    
    labels_file = '%s/labels.txt' % output_dir        
    parse_val_folder_args.append(val_image_path)
    parse_val_folder_args.append(labels_file)
    parse_val_folder_args.append('--val_file=%s' % val_file)
    parse_val_folder_args.append('--percent_val=100')

    tmp_parse_folder_args = []
    tmp_parse_folder_args += args
    tmp_parse_folder_args += parse_val_folder_args
    parse_val_folder_args = [str(x) for x in tmp_parse_folder_args]        
    logger.info('Parse Folder (val) subprocess args: "%s"' % ' '.join(parse_val_folder_args))         
    print "" 

    return parse_val_folder_args

"""
Create args for parse test folder subprocess
"""
def _create_parse_test_folder_args(args, output_dir, test_image_path, test_file):  
    parse_test_folder_args = []    
    labels_file = '%s/labels.txt' % output_dir        
    parse_test_folder_args.append(test_image_path)
    parse_test_folder_args.append(labels_file)
    parse_test_folder_args.append('--test_file=%s' % test_file)
    parse_test_folder_args.append('--percent_test=100')

    tmp_parse_folder_args = []
    tmp_parse_folder_args += args
    tmp_parse_folder_args += parse_test_folder_args
    parse_test_folder_args = [str(x) for x in tmp_parse_folder_args]        
    logger.info('Parse Folder (test) subprocess args: "%s"' % ' '.join(parse_test_folder_args))         
    print "" 

    return parse_test_folder_args
"""
"""                

def split(output_dir, train_images_path, val_images_path, test_images_path, percent_val, percent_test):
    # Get the args      
    logger.debug('Get the parameters for split: output_dir=(%s), train_images_path=(%s), val_images_path=(%s), test_images_path=(%s), percent_val=(%s), percent_test(%s)' 
        % (output_dir, train_images_path, val_images_path, test_images_path, percent_val, percent_test))
 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parse_folder_tool = '%s/parse_folder.py' % dir_path
    logger.debug('The parse folder tool is %s' % parse_folder_tool)

    # Define default parse folder args
    min_per_category = 2
    parse_folder_args = [sys.executable, parse_folder_tool,]
    parse_folder_args.append('--min=%s' % min_per_category)


    # Create args to parse train folder
    parse_train_folder_args = []
    if (train_images_path is not None):
        train_file = '%s/%s' % (output_dir, utils.constants.TRAIN_FILE)
        if percent_val:
            val_file = '%s/%s' % (output_dir, utils.constants.VAL_FILE)
        else:
            val_file = None
        if percent_test:
            test_file = '%s/%s' % (output_dir, utils.constants.TEST_FILE)
        else:
            test_file = None
                
        parse_train_folder_args = _create_parse_train_folder_args(parse_folder_args, output_dir, train_images_path, train_file, percent_val, val_file, percent_test, test_file)   

    # Create args to parse val folder
    parse_val_folder_args = []    
    if  (val_images_path is not None) and (len(val_images_path) > 0) and (val_file is None):
        val_file = '%s/%s' % (output_dir, utils.constants.VAL_FILE)
        parse_val_folder_args = _create_parse_val_folder_args(parse_folder_args, output_dir, val_images_path, val_file) 

    # Create args to parse test folder
    parse_test_folder_args = []   
    if  (test_images_path is not None) and (len(test_images_path) > 0):
        test_file = '%s/%s' % (output_dir, utils.constants.TEST_FILE)
        parse_test_folder_args = _create_parse_test_folder_args(parse_folder_args, output_dir, test_images_path, test_file)             

    # The args are ready, create subprocess now
    process_args_list = [parse_train_folder_args, parse_val_folder_args, parse_test_folder_args]
    common.create_subprocess(process_args_list)
    '''
    logger.info('The train file is: %s' % train_file)
    logger.info('The val file is: %s' % val_file)
    logger.info('The test file is: %s' % test_file)
    '''

    return train_file, val_file, test_file
