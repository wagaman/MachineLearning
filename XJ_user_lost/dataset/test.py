# -*- coding: utf-8 -*-

import sys
import os
import logging
#from pyspark import SparkContext
import argparse
import shutil

sys.path.insert(0,'/opt/ibm/bluemind/tools/dataset')

import frameworks.caffe as caffe_dataset
import frameworks.tensorflow as tensorflow_dataset
import utils.log
import utils.fun as fun
import utils.split as split
import utils.common as common

logger = logging.getLogger(__name__)

'''
Create dataset from image directory or txt file
'''
def _dataset_create():
    parser = argparse.ArgumentParser(
        #description='Create dataset',
        usage='''python main.py create [<args>]'''
        ) 

    # Positional arguments    
    parser.add_argument('output_dir',
                        help='Path to the output database')                   
    #TODO: double check this option
#    parser.add_argument(
#        'labels_file',
#        help=('The file containing labels. If train_file is set, this file '
#              'will be generated (output). Otherwise, this file will be read (input).')
#    )

    # Optional arguments
    parser.add_argument('-I', '--train_images_path',
        help='A filesystem path to the folder of train images'
    )
    parser.add_argument('-K', '--val_images_path',
        help='A filesystem path to the folder of val images'
    )
    parser.add_argument('-L', '--test_images_path',
        help='A filesystem path to the folder of test images'
    )    
    parser.add_argument(
        '-t', '--train_file',
        help='The output file for training images'
    )
    parser.add_argument(
        '-T', '--percent_train', type=float,
        help='Percent of images used for the training set (constant across all categories)'
    )
    parser.add_argument(
        '-v', '--val_file',
        help='The output file for validation images'
    )
    parser.add_argument(
        '-V', '--percent_val', type=float,
        help='Percent of images used for the validation set (constant across all categories)'
    )
    #TODO: select a meaningful char for test images output file
    parser.add_argument(
        '-x', '--test_file',
        help='The output file for test images'
    )
    parser.add_argument(
        '-X', '--percent_test', type=float,
        help='Percent of images used for the test set (constant across all categories)'
    )
    parser.add_argument('-W', '--width',
                        type=int,
                        help='width of resized images, set to 0 if images have already been resized'
                        )
    parser.add_argument('-H', '--height',
                        type=int,
                        help='height of resized images, set to 0 if images have already been resized'
                        )    
    parser.add_argument('-c', '--resize_type',
                        help='resize type for images (must be "grayscale", "color" [default])'
                        )
    parser.add_argument('-r', '--resize_mode',
                        help='resize mode for images (must be "crop", "squash" [default], "fill" or "half_crop")'
                        )
    parser.add_argument('-m', '--mean_file', action='append',
                        help="location to output the image mean (doesn't save mean if not specified)")
    parser.add_argument('-s', '--shuffle',
                        action='store_true',
                        help='Shuffle images before saving'
                        )
    parser.add_argument('-e', '--encoding',
                        help='Image encoding format (jpg/png)'
                        )
    parser.add_argument('-b', '--backend',
                        default='lmdb',
                        help='The database backend - lmdb[default], tfrecords')

    args = parser.parse_args(sys.argv[2:])
    # Get the args
    output_dir = args.output_dir
    val_images_path = args.val_images_path    
    test_images_path = args.test_images_path
    train_images_path = args.train_images_path
    val_file = args.val_file
    test_file = args.test_file   
    train_file = args.train_file  
    percent_val = args.percent_val
    percent_test= args.percent_test
    percent_train = args.percent_train
    min_per_category = 2
    #min_per_category = args.min
    #max_per_category = args.max
    width = args.width
    height = args.height
    backend = args.backend
    #backend = 'lmdb'
    encoding = args.encoding
    resize_mode = args.resize_mode
    resize_type = args.resize_type       

    # Initial output directory
    common.mkdir(output_dir, clean=True)

    # Split the dataset
    if (train_images_path is not None): # create dataset from images directory
        if (os.path.isdir(train_images_path)):
            train_file, val_file, test_file = split.split(output_dir, train_images_path, val_images_path, test_images_path, percent_val, percent_test) 
            logger.info('After split, the train_file is: %s' % train_file)
            logger.info('After split, the val_file is: %s' % val_file)
            logger.info('After split, the test_file is: %s' % test_file)
        else: # The train_images_path specifies a file, we will copy it as raw data
            logger.error('The train_images_path must be a directory.')
            sys.exit(1)
    else: # create dataset from txt file
        logger.debug('Copy the specified txt file to destition directory.')
        if (train_file is not None):
            common.copy(train_file, output_dir)
        if (val_file is not None):
            common.copy(val_file, output_dir)
        if (test_file is not None):
            common.copy(test_file, output_dir)            

    # Only 1 entry
    if backend == 'lmdb':
        caffe_dataset.main(output_dir, train_file, val_file, test_file, width, height,resize_type, resize_mode, encoding)
    elif backend == 'tfrecords':
        tensorflow_dataset.main(output_dir, train_file, val_file, test_file, width, height,resize_type, resize_mode, encoding)
    else:
        logger.error('The backend %s you specified is not supported.' % backend)

    # Temp fix for permission deny
    os.system('chown -R egoadmin:egoadmin ' + output_dir)

    spark.stop()

'''
Remove dataset in specified directory
'''
def _dataset_remove():
    parser = argparse.ArgumentParser(
        #description='Remove dataset',
        usage='''python main.py remove [<args>]'''
        )

    # NOT prefixing the argument with -- means it's not optional
    parser.add_argument('dataset_dir', help='The dataset top directory')
    args = parser.parse_args(sys.argv[2:])

    spark = SparkContext(appName="Bluemind Dataset Tool")
    logger.info('Remove the dataset directory: %s' % args.dataset_dir)
    common.rmdir(args.dataset_dir)
    spark.stop()

'''
Count label numbers
'''
def _dataset_statistic():
    parser = argparse.ArgumentParser(
        #description='Remove dataset',
        usage='''python main.py count dataset_dir [OPTION]
                -b, --backend   backend of the dataset'''
        )

    # NOT prefixing the argument with -- means it's not optional
    parser.add_argument('dataset_dir', help='The dataset top directory')
    parser.add_argument('-b', '--backend',
                        default='lmdb',
                        help='The database backend - lmdb[default], tfrecords')

    args = parser.parse_args(sys.argv[2:])

    dataset_dir = args.dataset_dir
    backend = args.backend

    spark = SparkContext(appName="Bluemind Dataset Tool")
    logger.info('Will count label numbers of dataset in directory: %s' % dataset_dir)

    if backend == 'lmdb':
        caffe_dataset.print_all_labels(dataset_dir + "/train_db", dataset_dir + "/val_db", dataset_dir + "/test_db")
    elif backend == 'tfrecords':
        # tensorflow_dataset.print_all_labels(dataset_dir + "/train_db", dataset_dir + "/val_db", dataset_dir + "/test_db")
        print ""
    else:
        logger.error('The backend %s you specified is not supported.' % backend)

    spark.stop()

'''
Import dataset and raw data
'''        
def _dataset_import():
    parser = argparse.ArgumentParser(
        #description='Remove dataset',
        usage='''python main.py import [<args>]'''
        )

    # NOT prefixing the argument with -- means it's not optional
    parser.add_argument('backend', help='The database backend')
    parser.add_argument('dest_dir', help='The dest directory')
    parser.add_argument('files', help='The files and directories to import, e.g.: file1,file2,dir1,dir2')
    args = parser.parse_args(sys.argv[2:])

    spark = SparkContext(appName="Bluemind Dataset Tool")
    logger.info('Import the dataset or raw data to directory: %s' % args.dest_dir)

    backend = args.backend

    # Initial dest directory
    dests = args.dest_dir.split(",")
    i = 0
    for dest in dests:
        common.mkdir(dest, clean=True)
    files = args.files.split(",")
    for file in files:
        common.copytree(file, dests[i])
        i += 1
    logger.info('Copy the dataset or raw data successfully')

    # train_file & val_outfile & test_outfile have same output directory
    output_dir = os.path.dirname(dests[0])
    if backend == 'lmdb':
        fun.save_labels_count('frameworks.caffe.core', output_dir)
    elif backend == 'tfrecords':
        fun.save_labels_count('frameworks.tensorflow.core', output_dir)
    else:
        logger.error('The backend %s you specified is not supported.' % backend)

    # Temp fix for permission deny
    os.system('chown -R egoadmin:egoadmin ' + output_dir)

    spark.stop()

'''
Main entry
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='''python main.py <action> [<args>]

The most commonly used actions are:
    import     Import dataset and raw data
    create     Create dataset from image directory or text file
    remove     Remove dataset
    count      Count the labels number
''')

    actions_list = ['import', 'create', 'remove', 'count']
    parser.add_argument('action', help='Action to run. Support import, create, remove, count actions only.')
    # parse_args defaults to [1:] need to validate specified action firstly
    args = parser.parse_args(sys.argv[1:2])
    if args.action not in actions_list:
        print 'Unrecognized action, run <python %s -h> to see the usage.' % (sys.argv[0])
        #parser.print_help()
        sys.exit(1)  

     
    # invoke method for special action
    if (args.action == 'import'): # import dataset
        _dataset_import()    
    if (args.action == 'create'): # create dataset
        _dataset_create()
    elif (args.action == 'remove'): # remove dataset
        _dataset_remove()
    elif (args.action == 'count'): # count lable numbers
        _dataset_statistic()
    else:
        sys.exit(0)
