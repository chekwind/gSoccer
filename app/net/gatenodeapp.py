#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from gfirefly.server.globalobject import GlobalObject,remoteserviceHandle

@remoteserviceHandle('gate')
def pushObject(topicID,msg,sendList):
	GLobalObject().netfactory.pushObject(topicID,msg,sendList)