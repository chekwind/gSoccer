#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from firefly.server.globalobject import GlobalObject
from firefly.netconnect.datapack import DataPackProtoc

dataprotocl = DataPackProtoc(78,37,38,48,9,0) #协议头
GlobalObject().netfactory.setDataProtocl(dataprotocl)

def loadModule():
	from app.share.dbopear import dbShieldWord
	from net import chat_net,chatnet
	from appinterface import chat

	dbShieldWord.getAll_ShieldWord()