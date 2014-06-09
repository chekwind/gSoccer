#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.game.gatenodeservice import remoteserviceHandle
from app.game.core.character.GamerCharacter import GamerCharacter
from app.game.core.GamersManager import GamersManager

@remoteserviceHandle
def enterPlace_601(dynamicId,characterId,placeId,force,gamer):
	'''进入场景'''
	if not gamer:
		gamer=GamerCharacter(characterId,dynamicId=dynamicId)
	GamersManager().addGamer(gamer)
	if not gamer.player.getPlayers():
		gamer.player.initBeginPlayer()
		gamer.CalPower()
	gamerinfo=gamer.formatInfo()
	responsedata={'result':True,'message':'','data':{'characterid':gamerinfo['id'],'power':gamerinfo['power'],'photo':gamerinfo['photo'],'repute':gamerinfo['repute'],'name':gamerinfo['nickname'],'level':gamerinfo['level'],'exp':gamerinfo['exp'],'maxexp':gamerinfo['maxExp'],'gamecoin':gamerinfo['gamecoin'],'coin':gamerinfo['coin'],'energy':gamerinfo['energy'],'trainpoint':gamerinfo['trainpoint'],'zenid':gamerinfo['zenid'],'tacticspoint':gamerinfo['tacticspoint'],'hasRole':True}}
	return responsedata