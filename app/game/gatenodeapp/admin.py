#coding:utf8
'''
Created on 2014-3-20

@author: CC
'''

from app.game.gatenodeservice import remoteserviceHandle
from app.game.core.GamersManager import GamersManager
from app.game.core.character.GamerCharacter import GamerCharacter

@remoteserviceHandle
def operagamer_99(pid,opera_str):
	'''执行后台管理脚本'''
	gamer=GamersManager().getGamerByID(pid)
	isOline=1
	if not gamer:
		gamer=GamerCharacter(pid)
		isOline=0
	exec(opera_str)
	if isOline==0:
		gamer.updateGamerDBInfo()