#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.game.core.GamersManager import GamersManager

def roleInfo(dynamicId,characterId):
	'''获取角色的状态栏信息
	@param userId: int 用户id
	@param characterId: 角色的id
	'''
	gamer=GamersManager().getGamerBydynamicId(dynamicId)
	if dynamicId!=gamer.getDynamicId():
		return {'result':False,'message':"角色不存在"}
	gamerinfo=gamer.formatInfo()
	responsedata={'result':True,'message':'','data':{'characterId':gamerinfo['id'],'rolename':gamerinfo['nickname'],'level':gamerinfo['level'],'exp':gamerinfo['exp'],'maxexp':gamerinfo['maxExp'],'gamecoin':gamerinfo['gamecoin'],'coin':gamerinfo['coin'],'energy':gamerinfo['energy'],'maxenergy':gamerinfo['energy'],'power':gamerinfo['power'],'photo':gamerinfo['photo'],'repute':gamerinfo['repute'],'trainpoint':gamerinfo['trainpoint'],'zenid':gamerinfo['zenid'],'tacticspoint':gamerinfo['tacticspoint']}}
	return responsedata

def calPower(dynamicId,characterId):
	''''''
	gamer=GamersManager().getGamerBydynamicId(dynamicId)
	if dynamicId!=gamer.getDynamicId():
		return {'result':False,'message':"角色不存在"}
	result=gamer.CalPower()
	return result
