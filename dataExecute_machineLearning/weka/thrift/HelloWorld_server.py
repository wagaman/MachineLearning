# coding: utf-8
__author__ = 'Administrator'
import socket
import sys

from weka.thrift import HelloWorld_thrift
from thrift.ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
class HelloWorldHandler:
    def sayHello(self, msg):
        ret = "Received: " + msg
        print(ret)
        return ret
#创建服务端
handler = HelloWorldHandler()
processor = HelloWorld_thrift.Processor(handler)
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