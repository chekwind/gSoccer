#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from gfirefly.server.globalobject import GlobalObject
from gfirefly.netconnect.datapack import DataPackProtoc

def callWhenConnLost(conn):
	dynamicId=conn.transport.sessionno
	GlobalObject().remote['gate'].callRemoteNotForResult("netconnlost",dynamicId)

GlobalObject().netfactory.doConnectionLost=callWhenConnLost
dataprotocl=DataPackProtoc(78,37,38,48,9,0)
GlobalObject().netfactory.setDataProtocl(dataprotocl)

def loadModule():
	import netapp
	import gatenodeapp	