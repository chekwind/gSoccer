#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from dataloader import load_config_data
from gfirefly.server.globalobject import GlobalObject
from app.game.core.GamersManager import GamersManager
from gtwisted.utils import log

def doWhenStop():
	"""服务器关闭前的处理
	"""
	for gamer in GamersManager()._gamers.values():
		try:
			gamer.updateGamerDBInfo()
			GamersManager().dropGamer(gamer)
		except Exception as ex:
			log.err(ex)

GlobalObject().stophandler=doWhenStop

def loadModule():
	"""
	"""
	load_config_data()
	from gatenodeapp import *