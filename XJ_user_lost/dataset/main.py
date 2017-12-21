# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import logging
from pyspark import SparkContext
import argparse
import shutil
import random
from subprocess import Popen, PIPE
import re
import xml.etree.ElementTree as ET
import cv2
import numpy as np
sys.path.insert(0,'/opt/ibm/bluemind/dlpd/tools/dataset')

import frameworks.caffe as caffe_dataset
import frameworks.tensorflow as tensorflow_dataset
import utils.log
import utils.fun as fun
import utils.split as split
import utils.common as common

import pandas as pd
from pandas import DataFrame

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

    spark = SparkContext(appName="Bluemind Dataset Tool")
    # Split the dataset
    if (train_images_path is not None): # create dataset from images directory
        if (os.path.isdir(train_images_path)):
            train_file, val_file, test_file = split.split(output_dir, train_images_path, val_images_path, test_images_path, percent_val, percent_test) 
            logger.info('After split, the train_file is: %s' % train_file)
            logger.info('After split, the val_file is: %s' % val_file)
            logger.info('After split, the test_file is: %s' % test_file)
        else: # The train_images_path specifies a file, we will copy it as raw data
            logger.error('The train_images_path must be a directory.')
            spark.stop()
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
        print("")
    else:
        logger.error('The backend %s you specified is not supported.' % backend)

    spark.stop()
    

 
'''
Import object dataset
'''        
def _dataset_object():
    parser = argparse.ArgumentParser(
        #description='import object dataset',
        usage='''python main.py object [<args>]'''
        )
        
    # Positional arguments    
    parser.add_argument('output_dir',
                        help='Path to the output database')                   

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
        '-T', '--percent_train', type=float,
        help='Percent of images used for the training set (constant across all categories)'
    )
    parser.add_argument(
        '-V', '--percent_val', type=float,
        help='Percent of images used for the validation set (constant across all categories)'
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
    parser.add_argument('-b', '--backend',
                        default='lmdb',
                        help='The database backend - lmdb[default], tfrecords')

    args = parser.parse_args(sys.argv[2:])
    # Get the args
    output_dir = args.output_dir
    val_images_path = args.val_images_path    
    test_images_path = args.test_images_path
    train_images_path = args.train_images_path 
    percent_val = args.percent_val
    percent_test= args.percent_test
    percent_train = args.percent_train
    min_per_category = 2
    width = args.width
    height = args.height
    backend = args.backend     

    # Initial output directory
    common.mkdir(output_dir, clean=True)
    common.mkdir(output_dir + "/ImageSets/Main", clean=True)
    common.mkdir(output_dir + "/Images", clean=True)
    common.mkdir(output_dir + "/Annotations", clean=True)
    common.mkdir(output_dir + "/JPEGImages", clean=True)
    
    spark = SparkContext(appName="Bluemind Dataset Tool")
    
    common.copytree(train_images_path+"/Annotations", output_dir+"/Annotations")
    common.copytree(train_images_path+"/JPEGImages", output_dir+"/JPEGImages")
    logger.info('Copy the object dataset successfully')

    
    
    # Split the dataset and draw rectangle
    lines = []
    image_dir=output_dir + "/JPEGImages"
    labels=[]
    labels.append("__background__")
    xml_dir=output_dir + "/Annotations"
    xScale=width/100
    yScale=height/100
    for dirpath, dirnames, filenames in os.walk(image_dir, followlinks=True):
            for filename in filenames:
                if (filename.find(".jpg")!=-1 or filename.find(".jpeg")!=-1 or filename.find(".npg")!=-1): 
                    (shortname,extension) = os.path.splitext(filename)
                    lines.append('%s' % (shortname))
                    
                    # rectangle and text
                    im = cv2.imread(image_dir+"/"+filename)
                    xmlfilename=output_dir + "/Annotations/" + shortname + ".xml"
                    tree = ET.parse(xmlfilename)
                    objs = tree.findall('object')
                    num_objs = len(objs)
                    for obj in objs:
                            bbox = obj.find('bndbox')
                            sx1 = bbox.find('xmin').text
                            sy1 = bbox.find('ymin').text
                            sx2 = bbox.find('xmax').text
                            sy2 = bbox.find('ymax').text
                            class_name = obj.find('name').text
                            if class_name not in labels:
                                labels.append('%s' % (class_name))
                            if (sy1 > 10):
                                cv2.putText(im, class_name, (int(sx1), int(sy1)-6), cv2.FONT_HERSHEY_COMPLEX_SMALL,0.8, (0, 255, 0) )
                            else:
                                cv2.putText(im, class_name, (int(sx1), int(sy1)+15), cv2.FONT_HERSHEY_COMPLEX_SMALL,0.8, (0, 255, 0) )
                            cv2.rectangle(im,(int(sx1), int(sy1)),(int(sx2), int(sy2)),(0,255,0),3)
                    res_img=output_dir + "/Images/" + filename
                    cv2.imwrite(res_img,im)  
                    
                    # resize
                    if (width != 0 and height != 0):
                        new_img = image_dir + "/resize-" + filename
                        
                        res = cv2.resize(im, None, None, fx=xScale, fy=yScale, interpolation=cv2.INTER_LINEAR)
                        cv2.imwrite(new_img,res)   
                        
                        # Add new picture to file list
                        lines.append('%s' % (shortname)) 
                        
                        # Add new xml file for the new picture
                        objs = tree.findall('object')
                        sizes = tree.findall('size')
                        num_objs = len(objs)
                        boxes = np.zeros((num_objs, 4), dtype=np.uint16)

                        #update size
                        for i, size in enumerate(sizes):
                            width1 = float(size.find('width').text)
                            height1 = float(size.find('height').text)
                            size.find('width').text = str(int(width1*xScale))
                            size.find('height').text = str(int(height1*yScale))

                        #update bbox
                        for ix, obj in enumerate(objs):
                            bbox = obj.find('bndbox')
                            sx1 = float(bbox.find('xmin').text)
                            sy1 = float(bbox.find('ymin').text)
                            sx2 = float(bbox.find('xmax').text)
                            sy2 = float(bbox.find('ymax').text)
                            txmin = sx1 * xScale
                            tymin = sy1 * yScale
                            txmax = sx2 * xScale
                            tymax = sy2 * yScale
                            boxes[ix, :] = [int(txmin), int(tymin), int(txmax), int(tymax)]
                            bbox.find('xmin').text = str(txmin)
                            bbox.find('ymin').text = str(tymin)
                            bbox.find('xmax').text = str(txmax)
                            bbox.find('ymax').text = str(tymax)
                            
                        #update filename
                        tree.find('filename').text="./JPEGImages/resize-" + filename
                        
                        res_xml = output_dir + "/Annotations/resize-" + shortname + ".xml"
                        tree.write(res_xml, encoding="utf-8",xml_declaration=True)
                           
                    
    train_lines = []
    val_lines = []
    test_lines = []
    
    random.shuffle(lines)
    image_num=len(lines)
    val_num=int ((image_num*percent_val)/100)
    test_num=int ((image_num*percent_test)/100)
    train_num=image_num-val_num-test_num
    
    train_lines = lines[:train_num]
    val_lines = lines[train_num:train_num+val_num]
    test_lines = lines[train_num+val_num:]
    
    train_file=output_dir +"/ImageSets/Main/train.txt"
    val_file=output_dir +"/ImageSets/Main/val.txt"
    test_file=output_dir +"/ImageSets/Main/test.txt"
    label_file=output_dir +"/ImageSets/Main/labels.txt"
    
    train_outfile = open(train_file, 'w')
    val_outfile = open(val_file, 'w')
    test_outfile = open(test_file, 'w')
    label_outfile = open(label_file, 'w')
    
    if train_lines:
        train_outfile.write('\n'.join(train_lines) + '\n')
    if val_lines:
        val_outfile.write('\n'.join(val_lines) + '\n')
    if test_lines:
        test_outfile.write('\n'.join(test_lines) + '\n')
    if labels:
        label_outfile.write('\n'.join(labels) + '\n')
    
    train_outfile.close()
    val_outfile.close()
    test_outfile.close()
    label_outfile.close()
    
    # Temp fix for permission deny
    os.system('chown -R egoadmin:egoadmin ' + output_dir)

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
        common.mkdir(dest, clean=False)
    files = args.files.split(",")
    for file in files:
        if os.path.isfile(file):
            common.copy(file, dests[i])
        else:
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
save structured tabular data as csv format
'''
def storeTransformedData(fpath_save, ds, **kw):
    if 'header' not in kw:
        kw['header'] = None
    if 'index' not in kw:
        kw['index'] = False

    print("Save transformed data to file \"%s\" which has shape %s...\n" % (fpath_save, ds.shape), ds)
    df = DataFrame(data = ds)
    df.info()
    df.to_csv(path_or_buf=fpath_save, **kw)

'''
Save ndarray to file with csv format
'''
def storeToDataset(fpath, data, recordShape, indexTuple):
    size_all = 1
    for x in np.array(data.shape): size_all *= x
    size_record = 1
    for x in np.array(recordShape): size_record *= x
    cnt_record = size_all // size_record
    size_valid = cnt_record * size_record
    print(dict(size_all=size_all, size_record=size_record, cnt_record=cnt_record, size_valid=size_valid))
    if size_valid < size_all:
        print('Cannot reshape exactly from %s to %s, drop %d items' % (
            data.shape, recordShape, size_all - size_valid), file=sys.stderr)

    # build index column
    index = indexTuple[1][:cnt_record]
    indexColumnName = indexTuple[0]
    df_index = DataFrame(index=index, data=index, columns=[indexColumnName])

    # drop unused data from input data to fit the shape, and
    # reshape to record shape
    data = data.reshape(-1)[:size_valid].reshape(cnt_record, size_record)

    # build data columns
    df_data = DataFrame(index=index, data=data)

    # consolidate the final table
    df = df_index.join(df_data)

    return storeTransformedData(fpath, df, header=df.columns)

'''
load ndarray from file with csv format
'''
def loadFromDataset(fpath, recordShape, index_col=0, header=0):
    df = pd.read_csv(fpath,
            header=header,
            index_col=index_col,
            comment='#',
            engine='c')
    # log for debug
    print('Data loaded from file \"%s\" has following content:' % fpath)
    df.info()

    #data = df.values.reshape(np.concatenate([[-1], np.array(recordShape)]))
    #return (data, (df.index.name, np.array(df.index)))
    return (df.values, (df.index.name, np.array(df.index)))

'''
Import csv dataset
'''
def _dataset_csv():
    parser = argparse.ArgumentParser(
        #description='import object dataset',
        usage='''python main.py csv [<args>]'''
    )

    # Positional arguments
    parser.add_argument('--output_dir', type=str,
         help='Path to the output database')
    # Optional arguments
    parser.add_argument('-I', '--train_data_path', type=str,
        help='A filesystem path to the folder of train data')
    parser.add_argument('-K', '--val_data_path', type=str,
        help='A filesystem path to the folder of val data')
    parser.add_argument('-L', '--test_data_path', type=str,
        help='A filesystem path to the folder of test data')
    parser.add_argument('-T', '--percent_train', type=float, default=1.0,
        help='Percent of data used for the training set (constant across all categories)')
    parser.add_argument('-V', '--percent_val', type=float, default=0.0,
        help='Percent of data used for the validation set (constant across all categories)')
    parser.add_argument('-X', '--percent_test', type=float, default=0.0,
        help='Percent of data used for the test set (constant across all categories)')

    args = parser.parse_args(sys.argv[2:])

    # if shuffle the data or not, default to true for now
    doShuffle = True

    # Initial output directory
    common.mkdir(args.output_dir, clean=True)
    common.mkdir(os.path.join(args.output_dir, 'train_db'), clean=True)
    common.mkdir(os.path.join(args.output_dir, 'val_db'), clean=True)
    common.mkdir(os.path.join(args.output_dir, 'test_db'), clean=True)

    spark = SparkContext(appName="Bluemind Dataset Tool csv import")
    logger.info('Import csv data and labels with arguments: %s' % args)

    '''
    def find_csv(dpath):
        for dirpath, dirnames, filenames in os.walk(dpath, followlinks=True):
            for filename in filenames:
                if (filename.find(".csv") != -1 or filename.find(".CSV")!= -1):
                    lines.append(os.path.join(dirpath, filename))
        return lines
    '''

    def read_X_seq(fpath, recordShape):
        X_seq, indexTup = loadFromDataset(fpath, recordShape, index_col=0, header=0)
        return X_seq, indexTup[1]

    def read_Y_seq(fpath, recordShape):
        X_seq, indexTup = loadFromDataset(fpath, recordShape, index_col=0, header=0)
        return X_seq, indexTup[1]

    def write_to_csv(fpath, data, index):
        storeToDataset(fpath, data, data[0].shape, ('sample_id', index))

    # this is the shape for index future case, lb60-la10-rf10
    # TODO: let's treat input data as single dimension
    X_shape = (60, 2)
    Y_shape = (2,)

    # load train data and label
    X_trn_fpath = os.path.join(args.train_data_path, 'data.csv')
    Y_trn_fpath = os.path.join(args.train_data_path, 'label.csv')
    X_trn, index_trn = read_X_seq(X_trn_fpath, X_shape)
    Y_trn, _ = read_Y_seq(Y_trn_fpath, Y_shape)

    # separate the train data based on the requested percentage
    cnt_trn = X_trn.shape[0]
    cnt_val = int(cnt_trn * args.percent_val / 100)
    cnt_tst = int(cnt_trn * args.percent_test / 100)
    logger.debug('cnt1 trn, val, tst = {} {} {}'.format(cnt_trn, cnt_val, cnt_tst))

    range_trn = range(X_trn.shape[0])
    if doShuffle: random.shuffle(range_trn)
    range_val = range_trn[0:cnt_val]
    range_tst = range_trn[cnt_val:cnt_val+cnt_tst]

    # load validation data
    if args.val_data_path is not None:
        X_val_fpath = os.path.join(args.val_data_path, 'data.csv')
        Y_val_fpath = os.path.join(args.val_data_path, 'label.csv')
        X_val, index_val = read_X_seq(X_val_fpath, X_shape)
        Y_val, _ = read_Y_seq(Y_val_fpath, Y_shape)

        if doShuffle:
            range_val = range(X_val.shape[0])
            random.shuffle(range_val)
            X_val = X_val[range_val, ...]
            Y_val = Y_val[range_val, ...]
            index_val = index_val[range_val, ...]
    else:
        X_val = X_trn[range_val, ...]
        Y_val = Y_trn[range_val, ...]
        index_val = index_trn[range_val, ...]

    # load test data
    if args.test_data_path is not None:
        X_tst_fpath = os.path.join(args.test_data_path, 'data.csv')
        Y_tst_fpath = os.path.join(args.test_data_path, 'label.csv')
        X_tst, index_tst = read_X_seq(X_tst_fpath, X_shape)
        Y_tst, _ = read_Y_seq(Y_tst_fpath, Y_shape)

        if doShuffle:
            range_tst = range(X_tst.shape[0])
            random.shuffle(range_tst)
            X_tst = X_tst[range_tst, ...]
            Y_tst = Y_tst[range_tst, ...]
            index_tst = index_tst[range_tst, ...]
    else:
        X_tst = X_trn[range_tst, ...]
        Y_tst = Y_trn[range_tst, ...]
        index_tst = index_trn[range_tst, ...]

    # re-pick train data
    range_trn = range_trn[cnt_val+cnt_tst:]
    X_trn = X_trn[range_trn, ...]
    Y_trn = Y_trn[range_trn, ...]
    index_trn = index_trn[range_trn, ...]

    logger.debug('cnt2 trn, val, tst = {} {} {}'.format(X_trn.shape, X_val.shape, X_tst.shape))

    # write out datasets
    X_trn_fpath = os.path.join(args.output_dir, 'train_db', 'data.csv')
    Y_trn_fpath = os.path.join(args.output_dir, 'train_db', 'label.csv')
    write_to_csv(X_trn_fpath, X_trn, index_trn)
    write_to_csv(Y_trn_fpath, Y_trn, index_trn)

    X_val_fpath = os.path.join(args.output_dir, 'val_db', 'data.csv')
    Y_val_fpath = os.path.join(args.output_dir, 'val_db', 'label.csv')
    write_to_csv(X_val_fpath, X_val, index_val)
    write_to_csv(Y_val_fpath, Y_val, index_val)

    X_tst_fpath = os.path.join(args.output_dir, 'test_db', 'data.csv')
    Y_tst_fpath = os.path.join(args.output_dir, 'test_db', 'label.csv')
    write_to_csv(X_tst_fpath, X_tst, index_tst)
    write_to_csv(Y_tst_fpath, Y_tst, index_tst)

    # Temp fix for permission deny
    os.system('chown -R egoadmin:egoadmin ' + args.output_dir)

    spark.stop()

'''
Main entry
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='''python main.py <action> [<args>]

The most commonly used actions are:
    import     Import dataset and raw data
    object     Import object dataset 
    csv        Import CSV dataset
    create     Create dataset from image directory or text file
    remove     Remove dataset
    count      Count the labels number
''')

    actions_list = ['import', 'create', 'remove', 'count', 'object', 'csv']
    parser.add_argument('action', help='Action to run. Support import, create, remove, count actions only.')
    # parse_args defaults to [1:] need to validate specified action firstly
    args = parser.parse_args(sys.argv[1:2])
    if args.action not in actions_list:
        print('Unrecognized action, run <python %s -h> to see the usage.' % (sys.argv[0]))
        #parser.print_help()
        sys.exit(1)  

    # invoke method for special action
    if (args.action == 'import'): # import dataset
        _dataset_import()  
    if (args.action == 'object'): # import object dataset
        _dataset_object()
    elif (args.action == 'csv'): # import csv dataset
        _dataset_csv()
    if (args.action == 'create'): # create dataset
        _dataset_create()
    elif (args.action == 'remove'): # remove dataset
        _dataset_remove()
    elif (args.action == 'count'): # count lable numbers
        _dataset_statistic()
    else:
        sys.exit(0)
