#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.game.gatenodeservice import remoteserviceHandle
from app.game.core.GamersManager import GamersManager
from gtwisted.utils import log

@remoteserviceHandle
def NetConnLost_2(dynamicId):
	'''loginout
	'''
	gamer=GamersManager().getGamerBydynamicId(dynamicId)
	if not gamer:
		return True
	try:
		gamer.updateGamerDBInfo()
		GamersManager().dropGamer(gamer)
		gamer.playerInner.dbupdate()
	except Exception as ex:
		log.err(ex)
	finally:
		return 	True