import math
import tensorflow as tf
from tensorflow.core.framework import summary_pb2

MAO_SUMMARIES_COLLECTION = 'mao_summaries'

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_boolean('SUMMARY_LOG', True, 'If true, output summary log for DLMAO.')

HIST_LIMIT4 = [float(i)/2 for i in range(-8, 8+1)] + [10000.0]
HIST_LIMIT2 = [float(i)/4 for i in range(-8, 8+1)] + [10000.0]
HIST_LIMIT1 = [float(i)/8 for i in range(-8, 8+1)] + [10000.0]


class MySummaryWriter(tf.summary.FileWriter):
    def __init__(self, logdir, graph=None, max_queue=10, flush_secs=120, graph_def=None):
        self._logdir = logdir
        super(MySummaryWriter, self).__init__(logdir, graph, max_queue, flush_secs, graph_def)
        
    def log_summary(self, summary, global_step=None):
        if type(summary) is str:
            summary_proto = summary_pb2.Summary()
            summary_proto.ParseFromString(summary)
        else:
            summary_proto = summary
        if FLAGS.SUMMARY_LOG:
            try:
                step = int(global_step)
            except:
                step = 0
            msg = "[%s] Iteration %d:" % (self._logdir, step)
            for v in summary_proto.value:
                if v.HasField('simple_value'):
                    print('%s tag %s, simple_value %f' % (msg, v.tag, v.simple_value))
                elif v.HasField('histo'):
#                     nozero = [limit for limit, count in zip(v.histo.bucket_limit, v.histo.bucket) if count > 0]
#                     if len(nozero) == 0:
#                         bucket_limit = HIST_LIMIT1
#                     else:
#                         lowest = math.floor(nozero[0])
#                         highest = math.ceil(nozero[-1])
#                         highest = max(abs(lowest), abs(highest))
#                         if highest <= 1: bucket_limit = HIST_LIMIT1
#                         elif highest <= 2: bucket_limit = HIST_LIMIT2
#                         else: bucket_limit = HIST_LIMIT4
                    bucket_limit = HIST_LIMIT2
                    bucket = [0] * len(bucket_limit)
                    current_bucket = 0
                    for limit, count in zip(v.histo.bucket_limit, v.histo.bucket):
                        if limit > bucket_limit[current_bucket]:
                            while current_bucket < len(bucket_limit) - 1:
                                current_bucket += 1
                                if (limit <= bucket_limit[current_bucket]): break;
                            if current_bucket >= len(bucket_limit): break
                        bucket[current_bucket] += count
                    bucket_limit = ' '.join(str(bl) for bl in bucket_limit)
                    bucket = ' '.join(str(b) for b in bucket)
                    print('%s tag %s, bucket_limit %s, bucket %s' % (msg, v.tag, bucket_limit, bucket))

    def add_summary(self, summary, global_step=None):
        self.log_summary(summary, global_step)
        super(MySummaryWriter, self).add_summary(summary, global_step)


# 1. add some functions: gradient, norm2, ratio, worst cases;
# 2. transparent namespace of monitor to user
# 3. universal interface for both summary and tf.contrib.learn.monitors
class CMonitor(object):
    def __init__(self, logDir, displayInterval, maxInteration):

        self._summaryDir = logDir
        self._trainSummaryWriter = None
        self._testSummaryWriter = None

        if tf.gfile.Exists(logDir):
            tf.gfile.DeleteRecursively(logDir)
        tf.gfile.MakeDirs(logDir)

        self._displayInterval = displayInterval
        self._maxInteration = maxInteration
        #self._layerNums = layerNums

        if maxInteration/10 > displayInterval*10: #need to implement further
            self._histDisplayInterval = displayInterval*10
        else:
            self._histDisplayInterval = maxInteration/10

        self._weight = {}
        self._bias = {}
        self._gradient = {}
        self._preactivation = {}
        self._activation = {}

        self._accuracyTrain = -1
        self._lossTrain = -1
        self._accuracyTest = -1
        self._lossTest = -1

        self._weightNorm2 = {}
        self._biasNorm2 = {}
        self._gradientNorm2 = {}
        self._preactivationNorm2 = {}
        self._activationNorm2 = {}

        self._ratio = {}

    def CreateTrainSummaryWriter(self, graph=None, max_queue=10, flush_secs=120, graph_def=None):
        if not self._trainSummaryWriter:
            _trainSummaryWriter = MySummaryWriter(self._summaryDir + '/train', graph, max_queue, flush_secs, graph_def)
        return _trainSummaryWriter

    def CreateTestSummaryWriter(self, graph=None, max_queue=10, flush_secs=120, graph_def=None):
        if not self._testSummaryWriter:
            _testSummaryWriter = MySummaryWriter(self._summaryDir + '/test', graph, max_queue, flush_secs, graph_def)
        return _testSummaryWriter

    def SummaryHist(self, name, value, layerIndex):
        if name == "weight":
            self._weight[layerIndex] = value
        elif name == "bias":
            self._bias[layerIndex] = value
        elif name =="gradient":
            self._gradient[layerIndex] = value
        elif name =="preactivation":
            self._preactivation[layerIndex] = value
        elif name == "activation":
            self._activation[layerIndex] = value
        else:
            print ("hist summary is only supported by weight/bias/gradient/preactivation/activation")
        histSummary = tf.summary.histogram(str(layerIndex) + "/" + name, value, [MAO_SUMMARIES_COLLECTION, tf.GraphKeys.SUMMARIES])
        return histSummary


    def SummaryScalar(self, name, value):
        if name == "train accuracy":
            self._accuracyTrain = value
        elif name == "test accuracy":
            self._accuracyTest = value
        elif name == "train loss":
            self._lossTrain = value
        elif name == "test loss":
            self._lossTest = value
        else:
            print ("scala summary is only supported by train/test accuracy/loss")
        scalarSummary = tf.summary.scalar(name, value, [MAO_SUMMARIES_COLLECTION, tf.GraphKeys.SUMMARIES])
        return scalarSummary


    def SummaryNorm2(self, name, value, layerIndex):
        norm2 = tf.sqrt(tf.reduce_sum(tf.square(value)))
        if name == "weight":
            self._weightNorm2[layerIndex] = norm2
        elif name == "bias":
            self._biasNorm2[layerIndex] = norm2
        elif name =="gradient":
            self._gradientNorm2[layerIndex] = norm2
        elif name == "preactivation":
            self._preactivationNorm2[layerIndex] = norm2
        elif name == "activation":
            self._activationNorm2[layerIndex] = norm2
        else:
            print ("norm summary is only supported by weight/bias/gradient/preactivation/activation")
        scalarSummary = tf.summary.scalar("norm2/" + str(layerIndex) + "/"+ name, norm2, [MAO_SUMMARIES_COLLECTION, tf.GraphKeys.SUMMARIES])
        return scalarSummary


    def SummaryGradient(self, name, loss):
        if name == "weight":
            for layerIndex in self._weight:
                self._gradient[layerIndex] = tf.gradients(loss, self._weight[layerIndex])
                self.SummaryHist("gradient", self._gradient[layerIndex], layerIndex)
                self.SummaryNorm2("gradient", self._gradient[layerIndex], layerIndex)
        elif name == "bias":
            for layerIndex in self._bias:
                self._gradient[layerIndex] = tf.gradients(loss, self._bias[layerIndex])
                self.SummaryHist("gradient", self._gradient[layerIndex], layerIndex)
                self.SummaryNorm2("gradient", self._gradient[layerIndex], layerIndex)
        elif name == "activation":
            for layerIndex in self._activation:
                self._gradient[layerIndex] = tf.gradients(loss, self._activation[layerIndex])
                self.SummaryHist("gradient", self._gradient[layerIndex], layerIndex)
                self.SummaryNorm2("gradient", self._gradient[layerIndex], layerIndex)
        else:
            print ("gradient summary is only supported by weight/bias/activation")



    def SummaryGWRatio(self):
        for layerIndex in self._weightNorm2:
            #print layerIndex
            #print self._gradientNorm2
            #print self._weightNorm2[layerIndex]
            self._ratio[layerIndex] = tf.divide(self._gradientNorm2[layerIndex], self._weightNorm2[layerIndex])
            tf.summary.scalar("ratio/" + str(layerIndex), self._ratio[layerIndex], [MAO_SUMMARIES_COLLECTION, tf.GraphKeys.SUMMARIES])
        #return scalarSummary


    def SummaryWorstCase(self):
        pass


