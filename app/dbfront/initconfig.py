#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from dataloader import registe_madmin,CheckMemDB,MAdminManager
from gfirefly.server.globalobject import GlobalObject

def doWhenStop():
	'''
	'''
	print "##############################"
	print "#######checkAdmins############"
	print "##############################"
	MAdminManager().checkAdmins()

GlobalObject().stophandler=doWhenStop

def loadModule():
	registe_madmin()
	CheckMemDB(1800)