#! /usr/bin/env python
'''Predict future index trend by using stateful RNNs
to model long sequences efficiently.
'''
from __future__ import print_function

import os
import sys
import subprocess
import argparse

from pkg_resources import parse_version

import pandas as pd
from pandas import DataFrame, Series, DatetimeIndex

import numpy as np
from sklearn import preprocessing

import keras
from keras import optimizers
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Dropout, Activation, TimeDistributed, LSTM
from keras.callbacks import TensorBoard, ModelCheckpoint

from keras import backend as K
from keras.objectives import categorical_crossentropy
from keras.metrics import categorical_accuracy

import tensorflow as tf

FLAGS = None
TF_FLAGS = None
# TF_FLAGS = tf.app.flags.FLAGS

PRI_PICK = lambda x, y: x if x is not None else y
# X dimention/number of input features
X_dim = 232
# Y dimention/number of classes
Y_dim = 2

DEFAULT_BACKEND = 'tensorflow_distribute'

'''
NOTE:
dlpd generate {train,val,test}_data in ps.conf when creating the model.
It traverse the directory and return a list of files.
Since we assume there are only {data,label}.csv two files in the directory and we
only need the directory name to be used in this model.
So, we back the dlpd return to its holding directory for process.
'''

DEFAULT_LOOKBACK = 3


DEFAULT_TEST_BATCHSIZE = 64


DEFAULT_CLIPNORM = 1.0   #指对梯度进行裁剪，通过控制梯度的最大范式，防止梯度爆炸的问题，是一种比较常用的梯度规约的方式。
DEFAULT_CLIPVALUE = 0.5   #keras:参数clipnorm和clipvalue是所有优化器都可以使用的参数,用于对梯度进行裁剪

DEFAULT_EPOCHS_PER_DECAY = 10

DEFAULT_MAX_TRAIN_EPOCHS = 20

DEFAULT_CKPT_DIR = './train'
DEFAULT_LOG_DIR= './log'
DEFAULT_LOG_DEVICE_PLACEMENT = False

DEFAULT_WEIGHT_FILE = ''

DEFAULT_MOMENTUM=0.9
DEFAULT_LR_DECAY=0.004
DEFAULT_LR=0.001
DEFAULT_TEST_INTERVAL=0.5
DEFAULT_MAX_TRAIN_STEPS=1000
DEFAULT_TRAIN_BATCHSIZE=64



DEFAULT_TEST_DS_PATH='/home/back_lyh/dataset/test4/test_db'
DEFAULT_TRAIN_DS_PATH='/home/back_lyh/dataset/test4/train_db'
DEFAULT_VALIDATION_DS_PATH='/home/back_lyh/dataset/test4/val_db'

'''
DEFAULT_TEST_DS_PATH='D:\\tmp\\tensorflow_test'
DEFAULT_TRAIN_DS_PATH='D:\\tmp\\tensorflow_train'
DEFAULT_VALIDATION_DS_PATH='D:\\tmp\\tensorflow_val'

'''



# save data to disk which had been loaded and transformed this time
# this will greatly reduce time
def storeTransformedData(fpath_save, ds, **kw):
    if 'header' not in kw:
        kw['header'] = None
    if 'index' not in kw:
        kw['index'] = False

    print("Save transformed data to file \"%s\" which has shape %s...\n" % (fpath_save, ds.shape), ds)
    df = DataFrame(data = ds)
    df.info()
    df.to_csv(path_or_buf=fpath_save, **kw)


def storeToDataset(fpath, data, recordShape, indexTuple):
    size_all = 1
    for x in np.array(data.shape): size_all *= x
    size_record = 1
    for x in np.array(recordShape): size_record *= x
    cnt_record = size_all // size_record
    size_valid = cnt_record * size_record
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


def loadFromDataset(fpath, recordShape, index_col=0, header=0):
    df = pd.read_csv(fpath,
            header=header,
            index_col=index_col,
            comment='#',
            engine='c')
    # log for debug
    print('Data loaded from file \"%s\" has following content:' % fpath)
    df.info()

    data = df.values.reshape(np.concatenate([[-1], np.array(recordShape)]))
    return (data, (df.index.name, np.array(df.index)))

# parse tensorflow specific arguments
def parseargs_tf():
    global TF_FLAGS

    parser = argparse.ArgumentParser()

    parser.add_argument('--ps_hosts', dest='ps_hosts', required=False, type=str,
                        help='Comma-separated list of hostname:port for the parameter server jobs')

    parser.add_argument('--log_dir', dest='log_dir', type=str, default=DEFAULT_LOG_DIR,
                        help='Tensorflow event log directory')
    parser.add_argument('--log_device_placement', dest='log_device_placement', type=bool, default=DEFAULT_LOG_DEVICE_PLACEMENT,
                        help='Whether to log device placement.')
    TF_FLAGS, unparsed = parser.parse_known_args()
    print({'TF_FLAGS': TF_FLAGS, 'unparsed': unparsed})


def loadData_tf():
    X_trn = None
    Y_trn = None
    X_val = None
    Y_val = None
    X_tst = None
    Y_tst = None

    # weight file is mandatory for inference and validation
    canReadWeightFile = os.access(FLAGS.weights + '.meta', os.R_OK)
    if not canReadWeightFile and FLAGS.maxTrainSteps < 1:
        print('Cannot inference or validate w/o a valid weight file, \"%s.{meta,index,data-*}\". Abort!' % '', FLAGS.weights)
        assert(False)

    if FLAGS.maxTrainSteps > 0:
        # mkdir -p <ckptDir>
        if not os.access(FLAGS.ckptDir, os.X_OK | os.W_OK):
            os.mkdir(FLAGS.ckptDir)

        # load train data
        if FLAGS.trainDS != '':
            fdat = os.path.join(FLAGS.trainDS, 'data.csv')
            flbl = os.path.join(FLAGS.trainDS, 'label.csv')
            X_trn, _ = loadFromDataset(fdat, (FLAGS.lookBack, X_dim))
            Y_trn, _ = loadFromDataset(flbl, (Y_dim,))
            print('X_trn has shape ', X_trn.shape)
            print('Y_trn has shape ', Y_trn.shape)

        else:
            print('No train dataset. Abort!')
            assert(False)

        # load validation data
        if FLAGS.validationDS != '':
            fdat = os.path.join(FLAGS.validationDS, 'data.csv')
            flbl = os.path.join(FLAGS.validationDS, 'label.csv')
            X_val, _ = loadFromDataset(fdat, (FLAGS.lookBack, X_dim))
            Y_val, _ = loadFromDataset(flbl, (Y_dim,))
            print('X_val has shape ', X_val.shape)
            print('Y_val has shape ', Y_val.shape)

        else:
            print('No validation dataset. Abort!')
            assert(False)

    # load test data
    if FLAGS.testDS != '':
        fdat = os.path.join(FLAGS.testDS, 'data.csv')
        flbl = os.path.join(FLAGS.testDS, 'label.csv')
        X_tst, _ = loadFromDataset(fdat, (FLAGS.lookBack, X_dim))
        Y_tst, _ = loadFromDataset(flbl, (Y_dim,))
        print('X_tst has shape ', X_tst.shape)
        print('Y_tst has shape ', Y_tst.shape)

    elif FLAGS.maxTrainSteps < 1:
        print('No test dataset. Abort!')
        assert(False)

    return X_trn, Y_trn, X_val, Y_val, X_tst, Y_tst


def main_tf(_):
    # parser TensorFlow specific arguments
    parseargs_tf()

    # setup TensorFlow distribute environment
    # NOTE: we only do this if there are more than 1 workers had been requested
    worker_hosts = []
    ps_hosts = []
    spec = {}


    if TF_FLAGS.ps_hosts is not None:
        ps_hosts = TF_FLAGS.ps_hosts.split(',')
        spec.update({'ps': ps_hosts})

    if len(worker_hosts) > 0:
        print('Cluster spec: ', spec)
        cluster = tf.train.ClusterSpec(spec)

        # Create and start a server for the local task.
        server = tf.train.Server(cluster, job_name=TF_FLAGS.job_name, task_index=TF_FLAGS.task_id)
        if TF_FLAGS.job_name == "ps":
            server.join()
    else:
        cluster = None
        server = tf.train.Server.create_local_server()
        # enforce a task_id for single node mode
        TF_FLAGS.task_id = 0

    # clean up event log directory in the chief task
    is_chief = (TF_FLAGS.task_id == 0) or (len(worker_hosts) < 2)
    if is_chief:
        if tf.gfile.Exists(TF_FLAGS.log_dir):
            tf.gfile.DeleteRecursively(TF_FLAGS.log_dir)
        tf.gfile.MakeDirs(TF_FLAGS.log_dir)

    # load data
    X_trn, Y_trn, X_val, Y_val, X_tst, Y_tst = loadData_tf()

    # tensor definition
    X_seq = tf.placeholder(tf.float32, shape=(None, FLAGS.lookBack, X_dim))
    Y_seq = tf.placeholder(tf.float32, shape=(None, Y_dim))#tf.placeholder：用于得到传递进来的真实的训练样本
    is_training = K.learning_phase()

    if True:
        # net
        x = LSTM(
            units=1000,
            return_sequences=True,
            stateful=False,
            batch_input_shape=(None, FLAGS.lookBack, X_dim),
            activation='sigmoid',
            recurrent_activation='hard_sigmoid')(X_seq) 
        x = LSTM(
            units=1000,
            return_sequences=False,
            stateful=False,
            activation='sigmoid',
            recurrent_activation='hard_sigmoid')(x)
        preds = Dense(Y_dim, activation='softmax')(x)

    # assign ops to the local worker by default.
    params = {}
    params['worker_device'] = "/job:worker/task:%d" % (TF_FLAGS.task_id)
    if cluster is not None:
        params['cluster'] = cluster
    with tf.device(tf.train.replica_device_setter(**params)):
        #worker_device="/job:worker/task:%d" % (TF_FLAGS.task_id),)):
        #cluster=cluster)):

        # loss
        loss = tf.reduce_mean(categorical_crossentropy(Y_seq, preds)) #categorical_crossentropy多分类的对数损失函数
        acc = tf.reduce_mean(tf.cast(categorical_accuracy(Y_seq, preds), tf.float32))
        global_step = tf.contrib.framework.get_or_create_global_step()

        # solver
        lr = tf.train.exponential_decay(FLAGS.lr,
            global_step,
            X_trn.shape[0] / FLAGS.trainBatchSize * FLAGS.epochsPerDecay,
            FLAGS.lrDecay,
            staircase=True)

        graph = tf.get_default_graph()
        train_op = tf.train.GradientDescentOptimizer(lr).minimize(loss,global_step=global_step)
		'''一个TensorFlow的运算，被表示为一个数据流的图。 
一         幅图中包含一些操作（Operation）对象，这些对象是计算节点。前面说过的Tensor对象，则是表示在不同的操作（operation）间的数据节点
           你一旦开始你的任务，就已经有一个默认的图已经创建好了。而且可以通过调用tf.get_default_graph()来访问到。
'''

    # train
    offset = 0

    # The StopAtStepHook handles stopping after running given steps.
    hooks=[
        tf.train.NanTensorHook(loss),
    ]

    def evaluate(sess, val_data, val_label):
        return sess.run([loss, acc], feed_dict={X_seq: val_data, Y_seq: val_label, is_training: 0})

    # Log trn/val loss and acc, and
    # trigger training stop
    class _LoggerHook(tf.train.SessionRunHook):
        def begin(self):
            self._next_trigger_step = FLAGS.testInterval
            self._trigger = False

        def before_run(self, run_context):
            args = {'global_step': global_step, 'acc': acc, 'loss': loss}
            if self._trigger:
                self._trigger = False
            return tf.train.SessionRunArgs(args)

        def after_run(self, run_context, run_values):
            gstep = run_values.results['global_step']
            trn_loss = run_values.results.get('loss', None)
            trn_acc = run_values.results.get('acc', None)

            if is_chief and gstep >= self._next_trigger_step:
                self._next_trigger_step += FLAGS.testInterval
                self._trigger = True

            # execute extra test operations after test interval
            summary = run_values.results.get('summary', None)
            if summary is not None:
                # write weights, gradient, activation summary

                # validate
                val_loss, val_acc = evaluate(run_context.session, X_val, Y_val)
                print("step: {}, trn_loss: {:.4f}, trn_acc: {:.4f}, val_loss: {:.4f}, val_acc: {:.4f}".format(
                    gstep,
                    trn_loss, trn_acc,
                    val_loss, val_acc))

                # write out for MAO
                test_summary = tf.Summary(value=[
                    tf.Summary.Value(tag='loss', simple_value=val_loss),
                    tf.Summary.Value(tag='accuracy', simple_value=val_acc),
                ])

            else:
                print("step: {}, trn_loss: {:.4f}, trn_acc: {:.4f}".format(
                    gstep,
                    trn_loss, trn_acc))

            if gstep >= FLAGS.maxTrainSteps:
                run_context.request_stop()

        def end(self, session):
            if is_chief and X_tst is not None and Y_tst is not None:
                val_loss, val_acc = evaluate(session, X_tst, Y_tst)
                print("Evaluation score at test dataset: loss: {:.4f}, acc: {:.4f}".format(val_loss, val_acc))

    if FLAGS.maxTrainSteps > 0:
        hooks.append(_LoggerHook())

    # Restore/save final weights at the begin/end of training
    class _SaveRestoreWeightsHook(tf.train.SessionRunHook):
        def __init__(self, weights, **kw):
            self._weights = weights
            self._saver_kw = kw

        def begin(self):
            self._saver = tf.train.Saver()

        def after_create_session(self, session, coord):
            # load last weight file
            if os.access(self._weights + '.meta', os.R_OK):
                self._saver.restore(session, self._weights)
                print('Restore weights file from \"%s\"' % self._weights)

        def end(self, session):
            if FLAGS.maxTrainSteps > 0:
                save_path = self._saver.save(session, self._weights, **self._saver_kw)
                print('Save weight file to \"%s\"' % save_path)

    # save final trained weights in chief task
    # NOTE:
    # - all parameters except weights are default, for now.
    #   https://www.tensorflow.org/api_docs/python/tf/train/Saver
    if is_chief and FLAGS.weights != '':
        hooks.append(_SaveRestoreWeightsHook(
            FLAGS.weights,
            global_step=None,
            latest_filename=None,
            meta_graph_suffix='meta',
            write_meta_graph=True
        ))

    # TODO: ckpt is still not working yet
    with tf.train.MonitoredTrainingSession(
        master=server.target,
        is_chief=is_chief,
        #checkpoint_dir=FLAGS.ckptDir,
        hooks=hooks,
        config=tf.ConfigProto(log_device_placement=TF_FLAGS.log_device_placement)
        ) as sess:

        K.set_session(sess)
        # NOTE:
        # - You might only need to save the graph once in order to
        #   find out the target tensor which need to be monitored by MAO, such as
        #   weights, bias, activations.
        # HOW:
        # - look at the "save/SaveV2/tensor_names" op and other activation tensor names
        #   from tensorboard
        #trainWriter.add_graph(sess.graph)

        while not sess.should_stop() and FLAGS.maxTrainSteps > 0:
            # start train interation loop
            while offset < X_trn.shape[0] - FLAGS.trainBatchSize:
                # pick up input data
                X_trn_batch = X_trn[offset:(offset + FLAGS.trainBatchSize), ...]
                Y_trn_batch = Y_trn[offset:(offset + FLAGS.trainBatchSize)]

                _ = sess.run(train_op, feed_dict={X_seq: X_trn_batch, Y_seq: Y_trn_batch, is_training: 1})

                # calculate next input batch
                offset += FLAGS.trainBatchSize

                if sess.should_stop(): break

            # next offset for next epochs
            offset %= X_trn.shape[0] - FLAGS.trainBatchSize

        # test only for validation procedure
        if is_chief and FLAGS.maxTrainSteps < 1 and X_tst is not None and Y_tst is not None:
            val_loss, val_acc = evaluate(sess, X_tst, Y_tst)
            print("Evaluation score at test dataset: loss: {:.4f}, acc: {:.4f}".format(val_loss, val_acc))


def main():
    if parse_version(keras.__version__) < parse_version('2.0.2'):
        print('Please upgrade \"keras\" to \"2.0.2\" or later.', file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser()
    parser.add_argument("--backend",
        action="store", dest="backend", type=str,
        default=DEFAULT_BACKEND, metavar="<tensorflow>",
        help="Default backend framework, default to \"%s\"" % (DEFAULT_BACKEND)
    )
    parser.add_argument("--weights",
        action="store", dest="weights", type=str,
        default=DEFAULT_WEIGHT_FILE, metavar="<ckpt_fpath>",
        help="Weight file to be saved or loaded, default to \"%s\"" % ('<ckpt_dir>/model.ckpt')
    )
    # use name "train_dir" to keep consistent with TensorFlow and BlueMind
    # it actually holds the ckpt data files
    parser.add_argument("--train_dir",
        action="store", dest="ckptDir", type=str,
        default=DEFAULT_CKPT_DIR, metavar="<train ckpt dir>",
        help="checkpoint directory to resume previous train and/or snapshot current train, default to \"%s\"" % (DEFAULT_CKPT_DIR)
    )
    parser.add_argument("--trainDS",
        action="store", dest="trainDS", type=str,
        default=DEFAULT_TRAIN_DS_PATH, metavar="<file path>",
        help="Train dataset, default to \"%s\"" % (DEFAULT_TRAIN_DS_PATH)
    )
    parser.add_argument("--validationDS",
        action="store", dest="validationDS", type=str,
        default=DEFAULT_VALIDATION_DS_PATH, metavar="<file path>",
        help="Validation dataset, default to \"%s\"" % (DEFAULT_VALIDATION_DS_PATH)
    )
    parser.add_argument("--testDS",
        action="store", dest="testDS", type=str,
        default=DEFAULT_TEST_DS_PATH, metavar="<file_path>",
        help="Test dataset, default to \"%s\"" % (DEFAULT_TEST_DS_PATH)
    )
    parser.add_argument("--lookBack",
        action="store", dest="lookBack", type=int,
        default=DEFAULT_LOOKBACK, metavar="<num>",
        help="Number of historical data records to be looked back, default to \"%d\"" % (DEFAULT_LOOKBACK)
    )
    parser.add_argument("--trainBatchSize",
        action="store", dest="trainBatchSize", type=int,
        default=DEFAULT_TRAIN_BATCHSIZE, metavar="<num>",
        help="Batch size for model train, default to \"%d\"" % (DEFAULT_TRAIN_BATCHSIZE)
    )
    parser.add_argument("--testBatchSize",
        action="store", dest="testBatchSize", type=int,
        default=DEFAULT_TEST_BATCHSIZE, metavar="<num>",
        help="Batch size for model test and validation, default to \"%d\"" % (DEFAULT_TEST_BATCHSIZE)
    )
    parser.add_argument("--maxTrainSteps",
        action="store", dest="maxTrainSteps", type=int,
        default=DEFAULT_MAX_TRAIN_STEPS, metavar="<num>",
        help="Maximum train steps, default to \"%d\"" % (DEFAULT_MAX_TRAIN_STEPS)
    )
    parser.add_argument("--testInterval",
        action="store", dest="testInterval", type=int,
        default=DEFAULT_TEST_INTERVAL, metavar="<num>",
        help="Test interval per train steps, default to \"%d\"" % (DEFAULT_TEST_INTERVAL)
    )
    parser.add_argument("--lr",
        action="store", dest="lr", type=float,
        default=DEFAULT_LR, metavar="<float>",
        help="Optimizer lr (learning rate), default to \"%f\"" % (DEFAULT_LR)
    )
    parser.add_argument("--epochsPerDecay",
        action="store", dest="epochsPerDecay", type=int,
        default=DEFAULT_EPOCHS_PER_DECAY, metavar="<num>",
        help="Number of epochs before decaying the learning rate, default to \"%d\"" % (DEFAULT_EPOCHS_PER_DECAY)
    )
    parser.add_argument("--lrDecay",
        action="store", dest="lrDecay", type=float,
        default=DEFAULT_LR_DECAY, metavar="<float>",
        help="Optimizer learning rate decay, default to \"%f\"" % (DEFAULT_LR_DECAY)
    )
    parser.add_argument("--momentum",
        action="store", dest="momentum", type=float,
        default=DEFAULT_MOMENTUM, metavar="<float>",
        help="Optimizer momentum, default to \"%f\"" % (DEFAULT_MOMENTUM)
    )
    parser.add_argument("--clipnorm",
        action="store", dest="clipnorm", type=float,
        default=DEFAULT_CLIPNORM, metavar="<float>",
        help="Optimizer clip norm, default to \"%f\"" % (DEFAULT_CLIPNORM)
    )
    parser.add_argument("--clipvalue",
        action="store", dest="clipvalue", type=float,
        default=DEFAULT_CLIPVALUE, metavar="<float>",
        help="Optimizer clip value, default to \"%f\"" % (DEFAULT_CLIPVALUE)
    )

    # parse input parameters
    global FLAGS
    FLAGS, unparsed = parser.parse_known_args()

    # default weight file to <ckpt_dir>/model.ckpt
    if FLAGS.weights == DEFAULT_WEIGHT_FILE:
        FLAGS.weights = os.path.join(FLAGS.ckptDir, 'model.ckpt')

    print({'FLAGS': FLAGS, 'unparsed': unparsed})

    if FLAGS.backend == 'tensorflow' or FLAGS.backend == 'tensorflow_distribute':
        tf.app.run(main=main_tf, argv=unparsed)

if __name__ == '__main__':
    main()