#coding:utf-8

import time

from socket import AF_INET,SOCK_STREAM,socket
from thread import start_new
import struct,json
HOST='172.16.2.169'
PORT=11010
BUFSIZE=1024
ADDR=(HOST , PORT)
client = socket(AF_INET,SOCK_STREAM)
client.connect(ADDR)

def sendData(sendstr,commandId):
    """78,37,38,48,9,0"""
    HEAD_0 = chr(78)
    HEAD_1 = chr(37)
    HEAD_2 = chr(38)
    HEAD_3 = chr(48)
    ProtoVersion = chr(9)
    ServerVersion = 0
    sendstr = sendstr
    data = struct.pack('!sssss3I',HEAD_0,HEAD_1,HEAD_2,\
                       HEAD_3,ProtoVersion,ServerVersion,\
                       len(sendstr)+4,commandId)
    senddata = data+sendstr
    return senddata

def resolveRecvdata(data):
    head = struct.unpack('!sssss3I',data[:17])
    lenght = head[6]
    data = data[17:17+lenght]
    return data




def chatlogin():
    client.sendall(sendData(json.dumps({"characterId":1000007,"roomId":2}),1001))
    print resolveRecvdata(client.recv(1024))
    sendmsg()

def sendmsg():
    client.sendall(sendData(json.dumps({"characterId":1000007,"roomId":2,"topic":1,"tonickname":"chekwind","content":"hello"}),1003))
    print resolveRecvdata(client.recv(1024))



    
#login()
#create()
#rolelogin()
chatlogin()



