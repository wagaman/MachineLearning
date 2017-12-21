# coding: utf-8
from weka.thrift import HelloWorld_thrift

__author__ = 'Administrator'
import sys
sys.path.append('./gen-py')



from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

try:
    #建立socket
    transport = TSocket.TSocket('localhost', 9090)
    #选择传输层，这块要和服务端的设置一致
    transport = TTransport.TBufferedTransport(transport)
    #选择传输协议，这个也要和服务端保持一致，否则无法通信
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    #创建客户端
    client = HelloWorld_thrift.Client(protocol)
    transport.open()

    print("client - say")
    msg = client.sayHello("Hello!")
    print("server - " + msg)
    #关闭传输
    transport.close()
#捕获异常
except Thrift.TException as ex:
    print("%s" % (ex.message))