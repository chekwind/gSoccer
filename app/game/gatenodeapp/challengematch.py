#coding:utf8
'''
Created on 2014-3-12

@author: CC
'''
from app.game.gatenodeservice import remoteserviceHandle
from app.game.appinterface import challengematch
import json

@remoteserviceHandle
def getChallengeMatchInfoByLeague_1201(dynamicId,request_proto):
	'''根据级别获取巡回赛npc信息'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	leagueindex=argument.get('leagueindex')
	response=challengematch.getChallengeMatchInfoByLeague(dynamicId,characterId,leagueindex)
	return json.dumps(response)