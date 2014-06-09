#coding:utf8
'''
Created on 2014-3-12

@author: CC
'''
from app.game.gatenodeservice import remoteserviceHandle
from app.game.appinterface import trainmatch
import json

@remoteserviceHandle
def getTrainMatchInfoByLeague_1101(dynamicId,request_proto):
	'''根据级别获取训练赛npc信息'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	leagueindex=argument.get('leagueindex')
	response=trainmatch.getTrainMatchInfoByLeague(dynamicId,characterId,leagueindex)
	return json.dumps(response)

@remoteserviceHandle
def doMatch_1102(dynamicId,request_proto):
	'''根据级别获取训练赛npc信息'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	npcid=argument.get('npcid')
	response=trainmatch.doMatch(dynamicId,characterId,npcid)
	return json.dumps(response)