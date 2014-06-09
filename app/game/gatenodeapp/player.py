#coding:utf8
'''
Created on 2014-2-8

@author: CC
'''
from app.game.gatenodeservice import remoteserviceHandle
from app.game.appinterface import player
from app.game.core.character.GamerCharacter import GamerCharacter
import json

@remoteserviceHandle
def playerListInfo_401(dynamic,request_proto):
	'''获取角色的球员列表'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	response=player.playerListInfo(dynamic,characterId)
	return json.dumps(response)

@remoteserviceHandle
def playerTraining_402(dynamic,request_proto):
	'''球员训练'''
	argument=json.loads(request_proto)
	characterid=argument.get('characterId')
	playerid=argument.get('playerid')
	Shoot=argument.get('shoot')
	Dribbling=argument.get('dribbling')
	Speed=argument.get('speed')
	Pass=argument.get('pass')
	Tackle=argument.get('tackle')
	Tackling=argument.get('tackling')
	_Save=argument.get('save')
	Response=argument.get('response')
	Trainpoint=argument.get('trainpoint')
	response=player.playertraining(dynamic,characterid,Shoot,Dribbling,Speed,Pass,Tackle,Tackling,_Save,Response,playerid,Trainpoint)
	return json.dumps(response)

@remoteserviceHandle
def addPlayerExp_403(dynamic,request_proto):
	'''球员加经验'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	playerid=argument.get('playerid')
	exp=argument.get('exp')
	response=player.addPlayerExp(dynamic,characterId,playerid,exp)
	return json.dumps(response)

@remoteserviceHandle
def upgradePlayer_404(dynamic,request_proto):
	'''球员升级'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	playerid=argument.get('playerid')
	gamecoin=argument.get('gamecoin')#消耗金币
	itemid=argument.get('itemid')#消耗道具
	response=player.upgradePlayer(dynamic,characterId,playerid,gamecoin,itemid)
	return json.dumps(response)

@remoteserviceHandle
def addPlayer_405(dynamic,request_proto):
	'''添加球员'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	templateId=argument.get('templateId')
	response=player.signPlayer(dynamic,characterId,templateId)
	return json.dumps(response)

@remoteserviceHandle
def dropPlayer_406(dynamic,request_proto):
	'''解雇球员'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	playerId=argument.get('playerId')
	response=player.dropPlayer(dynamic,characterId,playerId)
	return json.dumps(response)

@remoteserviceHandle
def getPlayerInner_407(dynamic,request_proto):
	'''获取球员大厅'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	response=player.getPlayerInner(dynamic,characterId)
	return json.dumps(response)

@remoteserviceHandle
def pickPlayer_408(dynamic,request_proto):
	'''获取球员大厅'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	picktype=argument.get('picktype')
	costpoint=argument.get('costpoint')
	leagueindex=argument.get('leagueindex')
	response=player.PickPlayer(dynamic,characterId,picktype,leagueindex,costpoint)
	return json.dumps(response)

@remoteserviceHandle
def dissmissPlayer_409(dynamic,request_proto):
	'''遣散球员大厅球员'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	playerId=argument.get('playerId')
	response=player.DissmissPlayer(dynamic,characterId,playerId)
	return json.dumps(response)

@remoteserviceHandle
def rotatePlayer_410(dynamic,request_proto):
	'''球员轮换'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	mainPlayerId=argument.get('mainPlayerId')
	benchPlayerId=argument.get('benchPlayerId')
	response=player.RotatePlayer(dynamic,characterId,mainPlayerId,benchPlayerId)
	return json.dumps(response)

@remoteserviceHandle
def signPlayer_411(dynamic,request_proto):
	'''遣散球员大厅球员'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	playerId=argument.get('playerId')
	gamecoin=argument.get('gamecoin')
	response=player.SignPlayer(dynamic,characterId,playerId,gamecoin)
	return json.dumps(response)

