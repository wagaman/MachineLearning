# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
import logging
import time
import logging
import platform
import subprocess
import lmdb
sys.path.insert(0,'/opt/ibm/bluemind/dlpd/tools/dataset')
import utils.fun as fun
import utils.constants
import utils.common as common

logger = logging.getLogger("caffe.core")

caffe_home = '_CAFFE_HOME_/caffe-public'
convert_imageset_tool = '%s/build/tools/convert_imageset' % caffe_home
compute_image_mean_tool = '%s/build/tools/compute_image_mean' % caffe_home
#TODO: Require Caffe Python API compiled
sys.path.insert(0, '%s/python' % caffe_home)
from caffe.proto import caffe_pb2

def _getCaffeHome():
    """Get Caffe installation path"""
    return 'The caffe home is: %s' % '/opt/caffe'

"""
Create args for create train db subprocess
"""
def _create_train_db_args(args, output_dir, train_file, width, height):
    train_db = '%s/%s' % (output_dir, utils.constants.TRAIN_DB)   
    train_db_args = []
    train_db_args += args
    train_db_args.append('/')
    train_db_args.append('%s' % train_file)
    train_db_args.append('%s' % train_db)
    train_db_args = [str(x) for x in train_db_args]        
    logger.info('Create DB (train) subprocess args: "%s"' % ' '.join(train_db_args))
    print ""

    return train_db_args

"""
Create args for create train db subprocess
"""
def _create_val_db_args(args, output_dir, val_file, width, height):
    val_db = '%s/%s' % (output_dir, utils.constants.VAL_DB)
    val_db_args = []
    val_db_args += args
    val_db_args.append('/')
    val_db_args.append('%s' % val_file)
    val_db_args.append('%s' % val_db)
    val_db_args = [str(x) for x in val_db_args]        
    logger.info('Create DB (val) subprocess args: "%s"' % ' '.join(val_db_args))
    print ""

    return val_db_args             

"""
Create args for create test db subprocess
"""
def _create_test_db_args(args, output_dir, test_file, width, height):
    test_db = '%s/%s' % (output_dir, utils.constants.TEST_DB)
    test_db_args = []
    test_db_args += args
    test_db_args.append('/')
    test_db_args.append('%s' % test_file)
    test_db_args.append('%s' % test_db)
    test_db_args = [str(x) for x in test_db_args]        
    logger.info('Create DB (test) subprocess args: "%s"' % ' '.join(test_db_args))
    print ""

    return test_db_args

"""
Create mean.binaryproto file
"""
def _create_mean_args(output_dir):
    mean_file = '%s/mean.binaryproto' % output_dir
    train_db = '%s/%s' % (output_dir, utils.constants.TRAIN_DB)
    mean_file_args =[compute_image_mean_tool, train_db, mean_file,]
    mean_file_args = [str(x) for x in mean_file_args]
    logger.info('Create mean file (mean.binaryproto) subprocess args: "%s"' % ' '.join(mean_file_args))
    print ""

    return mean_file_args


"""
Count indexes of the lmdb file.
Return a map in format:
    {
        label1 : n1,
        label2 : n2,
        ...,
        labeln : nn
    }
If the lmdb_file does NOT exist, return an empty map.

Callback this function from fun.save_labels_count().
"""
def count_indexes(lmdb_file):
    indexes = {}
    if os.path.exists(lmdb_file):
        logger.info('Count indexes of "%s".' % lmdb_file)
        lmdb_env = lmdb.open(lmdb_file)
        lmdb_txn = lmdb_env.begin()
        lmdb_cursor = lmdb_txn.cursor()
        datum = caffe_pb2.Datum()
        for key, value in lmdb_cursor:
            datum.ParseFromString(value)
            index = datum.label
            num = indexes.get(index, 0)
            indexes[index] = num + 1
    else:
        logger.info('The lmdb file "%s" does NOT exist.' % lmdb_file)
    return indexes


"""
"""

def main(output_dir, train_file, val_file, test_file, width, height,resize_type, resize_mode, encoding):
    # Get the args      
    logger.debug('Get the parameters to convert LMDB: output_dir=(%s), train_file=(%s), val_file=(%s), test_file=(%s), width=(%s), height=(%s), resize_type=(%s), resize_model=(%s), encoding=(%s)' 
    	% (output_dir, train_file, val_file, test_file, width, height,resize_type, resize_mode, encoding))

    
    # Define default create db args
    create_db_args = [convert_imageset_tool, ]
    create_db_args.append('--resize_height=%s' % height)
    create_db_args.append('--resize_width=%s' % width)
    if resize_type == 'grayscale':
        create_db_args.append('--gray=true')
    create_db_args.append('--shuffle')                

    # Create args to create train db
    train_db_args = []
    if train_file:
        train_db_args = _create_train_db_args(create_db_args, output_dir, train_file, width, height)

    # Create mean file args
    mean_file_args = _create_mean_args(output_dir)
    
    # Create args to create val db
    val_db_args = []
    if val_file:
        val_db_args = _create_val_db_args(create_db_args, output_dir, val_file, width, height)     

    # Create args to create test db
    test_db_args = []
    if test_file:
        test_db_args = _create_test_db_args(create_db_args, output_dir, test_file, width, height)      

    # The args are ready, create subprocess now
    process_args_list = [train_db_args, val_db_args, test_db_args, mean_file_args]
    common.create_subprocess(process_args_list)

    # Save labels count
    fun.save_labels_count("frameworks.caffe.core", output_dir)
