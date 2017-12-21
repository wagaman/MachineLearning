# -*- coding: utf-8 -*-
import os
import os.path
import sys
import logging
sys.path.insert(0,'/opt/ibm/bluemind/dlpd/tools/dataset')
import tensorflow as tf
import numpy as np
try:
    import cv2
except:
    pass
import utils.fun as fun

logger = logging.getLogger("tensorflow.core")

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def load_label_file(examples_list_file):
    examples = []
    labels = []
    for line in open(examples_list_file):
        data = line.strip().split(' ')
        examples.append(data[0])
        labels.append(int(data[1]))
    return np.asarray(examples), np.asarray(labels)

def extract_image(filename,  resize_height, resize_width):
    image = cv2.imread(filename)
    if resize_height != 0 and resize_width != 0:
        image = cv2.resize(image, (resize_height, resize_width))
    b,g,r = cv2.split(image)      
    rgb_image = cv2.merge([r,g,b])    
    return rgb_image

def convert2TFRecords(train_file, name, output_directory, resize_height, resize_width):
    output_directory = output_directory + "/" + name + '_db'
    if not os.path.exists(output_directory) or os.path.isfile(output_directory):
        os.makedirs(output_directory)
    _examples, _labels = load_label_file(train_file)
    filename = output_directory + "/" + 'data.tfrecords'
    writer = tf.python_io.TFRecordWriter(filename)
    for i, [example, label] in enumerate(zip(_examples, _labels)):
        image = extract_image(example, resize_height, resize_width)
        image_raw = image.tostring()
        example = tf.train.Example(features=tf.train.Features(feature={
            'image_raw': _bytes_feature(image_raw),
            'height': _int64_feature(image.shape[0]),
            'width': _int64_feature(image.shape[1]),
            'depth': _int64_feature(image.shape[2]),
            'label': _int64_feature(label)
        }))
        writer.write(example.SerializeToString())
    writer.close()

def read_tfrecord(filename_queuetemp):
    filename_queue = tf.train.string_input_producer([filename_queuetemp])
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(
        serialized_example,
        features={
          'image_raw': tf.FixedLenFeature([], tf.string),
          'width': tf.FixedLenFeature([], tf.int64),
          'depth': tf.FixedLenFeature([], tf.int64),
          'label': tf.FixedLenFeature([], tf.int64)
      }
    )
    image = tf.decode_raw(features['image_raw'], tf.uint8)
    tf.reshape(image, [256, 256, 3])
    image = tf.cast(image, tf.float32) * (1. /255) - 0.5
    label = tf.cast(features['label'], tf.int32)
    return image, label

def count_lable(filename_queuetemp):
    filename_queue = tf.train.string_input_producer([filename_queuetemp])
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(
        serialized_example,
        features={
          'image_raw': tf.FixedLenFeature([], tf.string),
          'width': tf.FixedLenFeature([], tf.int64),
          'depth': tf.FixedLenFeature([], tf.int64),
          'label': tf.FixedLenFeature([], tf.int64)
      }
    )
    image = tf.decode_raw(features['image_raw'], tf.uint8)
    tf.reshape(image, [256, 256, 3])
    image = tf.cast(image, tf.float32) * (1. /255) - 0.5
    label = tf.cast(features['label'], tf.int32)
    return image, label


"""
Count indexes of the tfrecords file.
Return a map in format:
    {
        label1 : n1,
        label2 : n2,
        ...,
        labeln : nn
    }
If the tfrecords_file does NOT exist, return an empty map.

Callback this function from fun.save_labels_count().
"""
def count_indexes(tfrecords_file):
    indexes = {}
    tfrecords_file = '%s/data.tfrecords' % tfrecords_file
    if os.path.exists(tfrecords_file):
        logger.info('Count indexes of "%s".' % tfrecords_file)
        for serialized_example in tf.python_io.tf_record_iterator(tfrecords_file):
            example = tf.train.Example()
            example.ParseFromString(serialized_example)
            index = example.features.feature['label'].int64_list.value[0]
            num = indexes.get(index, 0)
            indexes[index] = num + 1
    else:
        logger.info('The tfrecords file "%s" does NOT exist.' % tfrecords_file)
    return indexes


#Input args:
#   output_dir,
#   train_file,
#   val_file,
#   test_file,
#   width,
#   height,
#   resize_type, resize_mode, encoding
def main(output_dir,train_file,val_file,test_file,width,height,resize_type,resize_mode,encoding):
    if train_file:
        convert2TFRecords(train_file,'train',output_dir,height,width)
    if val_file:
        convert2TFRecords(val_file,'val',output_dir,height,width)
    if test_file:
        convert2TFRecords(test_file,'test',output_dir,height,width)

    # Save labels count
    fun.save_labels_count('frameworks.tensorflow.core', output_dir)


if __name__ == '__main__':
    main(output_dir='./',train_file='./train.txt',val_file='./val.txt',width=28,height=28,test_file='',resize_type='',resize_mode='',encoding='')
