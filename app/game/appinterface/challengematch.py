#coding:utf8
'''
Created on 2014-3-12

@author: CC
'''

from app.game.core.GamersManager import GamersManager

def getChallengeMatchInfoByLeague(dynamicId,characterId,leagueindex):
	'''根据级别获取挑战赛赛npc信息'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	data=gamer.challengematch.getNpcByLeague(leagueindex)
	return {'result':True,'data':data}