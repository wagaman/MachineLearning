# coding: utf-8

__author__ = 'Administrator'
import socket
import sys
sys.path.append('./gen-py')
from weka.thrift import train_and_pre_Thrift
from ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from weka.thrift import classify_service as cs

class train_and_preHandler:
    models = {}
    def getModel(self, trainPath, testPath):
        print(trainPath)
        print(testPath)
        dict = cs.getRandomForest(trainPath, testPath)
        self.models[dict['id']] = dict['model']
        return dict
    def predict_one(self, data):
        ret = "Received: "
        print(data)
        return ret

if __name__ == '__main__':
    #创建服务端
    handler = train_and_preHandler()
    processor = train_and_pre_Thrift.Processor(handler)
    #监听端口
    transport = TSocket.TServerSocket("127.0.0.1", 9091)
    #选择传输层
    tfactory = TTransport.TBufferedTransportFactory()
    #选择传输协议
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    #创建服务端
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    print("Starting thrift server in python...")
    server.serve()
    print("done!")