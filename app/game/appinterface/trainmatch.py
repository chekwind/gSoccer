#coding:utf8
'''
Created on 2014-3-12

@author: CC
'''

from app.game.core.GamersManager import GamersManager

def getTrainMatchInfoByLeague(dynamicId,characterId,leagueindex):
	'''根据级别获取训练赛npc信息'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	data=gamer.trainmatch.getNpcByLeague(leagueindex)
	return {'result':True,'data':data}

def doMatch(dynamicId,characterId,npcid):
	''''''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	data=gamer.trainmatch.doMacth(npcid)
	return {'result':True,'data':data}