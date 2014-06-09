#coding:utf8
'''
Created on 2014-2-7

@author: CC
'''

from app.game.core.GamersManager import GamersManager
from app.share.dbopear import dbPlayer
from app.game.component.player import PlayerInner

def playerListInfo(dynamicId,characterId):
	'''获取角色的球员列表'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	playerList=gamer.player.FormatPlayerList()
	return {'result':True,'data':playerList}

def playertraining(dynamicId,characterId,Shoot,Dribbling,Speed,Pass,Tackle,Tackling,_Save,Response,playerid,Trainpoint):
	'''球员训练'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	result=gamer.player.PlayerTraining(playerid,Shoot,Dribbling,Speed,Pass,Tackle,Tackling,_Save,Response,Trainpoint,gamer)
	return result

def addPlayerExp(dynamicId,characterId,playerid,exp):
	'''球员加经验'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	result=gamer.player.addPlayerExp(playerid,exp)
	return result

def upgradePlayer(dynamicId,characterId,playerid,gamecoin,itemid):
	'''球员升级'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	if gamer.finance.addGameCoin(-gamecoin):
		result=gamer.player.upgradePlayer(playerid)
		return result
	else:
		return {'result':False,'message':u"银币不足"}

def addPlayer(dynamicId,characterId,templateId):#添加新球员到替补席
	'''添加新球员到替补席'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	result=gamer.player.addPlayer(templateId)
	return result

def dropPlayer(dynamicId,characterId,playerid):#尚未添加返还训练点
	'''解雇球员'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	result=gamer.player.DropPlayer(playerid)
	if result:		
		# returnpoint=PlayerInner.DISSMISSPOINT.get(playerquality) 查询训练点
		# gamer.playerInner.updatePoint(returnpoint) 返还训练点
		return {'result':True,'message':""}
	else:
		return {'result':False,'message':u"解雇失败"}

def getPlayerInner(dynamicId,characterId):
	'''获取球员寻找信息'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	data={}
	pi=gamer.playerInner
	data['xy']=pi.xy
	data['ctime1']=pi.getTime(1)
	data['ctime2']=pi.getTime(2)
	data['cs1']=pi.cs1
	data['cs2']=pi.cs2
	data['player1']=pi.inner[0]
	data['player2']=pi.inner[1]
	data['player3']=pi.inner[2]
	data['point']=pi.point
	return {'result':True,'data':data}

def PickPlayer(dynamicId,characterId,picktype,leagueindex,costpoint=0):
	'''挑选球员'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	info=gamer.playerInner.pickPlayer(picktype,costpoint,leagueindex)
	if info.get('result'):
		playerid=info.get('data').get('playerid')
		player=gamer.player.addPlayer(playerid,1,3)
		if player==-1:
			return {'result':False,'message':u"替补席已满"}
		elif player==-2:
			return {'result':False,'message':u"球员大厅已满"}
		else:
			info['data']['player']=player.formatPlayerInfo()
	else:
		return info
	return {'result':True,'data':info.get('data')}

def DissmissPlayer(dynamicId,characterId,playerid):
	'''遣散球员'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	player=gamer.player.getPlayer(playerid)
	playerquality=player.level.getPlayerQuality()
	result=gamer.player.DropPlayer(playerid)
	if result:		
		returnpoint=PlayerInner.DISSMISSPOINT.get(playerquality)
		gamer.playerInner.updatePoint(returnpoint)
		return {'result':True,'message':""}
	else:
		return {'result':False,'message':u"遣散失败"}

def RotatePlayer(dynamicId,characterId,mainPlayerid,benchPlayerid):
	'''球员轮换'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	mainplayer=gamer.player.getPlayer(mainPlayerid)
	benchplayer=gamer.player.getPlayer(benchPlayerid)
	if mainplayer and benchplayer:
		maintempID=mainplayer.templateInfo.get('id')
		bebchtempID=benchplayer.templateInfo.get('id')
		if not gamer.player.IsOnCourt(bebchtempID,benchPlayerid) or maintempID==bebchtempID:
			playertemps=gamer.player.getPlayers()
			mainpos=mainplayer.getPlayerpos()
			benchpos=benchplayer.getPlayerpos()
			maincategory=mainplayer.getPlayerCategory()
			benchcategory=benchplayer.getPlayerCategory()
			mainplayer.savePlayerpos(benchpos,benchcategory)
			benchplayer.savePlayerpos(mainpos,maincategory)
			players=[]
			for player in gamer.player.getPlayers().values():
				if player.getPlayerpos()>='a' and player.getPlayerpos()<'z':#场上球员
					info=player.formatPlayerInfo()
					players.append(info)
			if len(players)!=11:#球员不是11人
				gamer.player._players=playertemps
				return {'result':False,'message':u"换人失败"}
			gamer.CalPower()
			return {'result':True,'message':u""}
		else:
			return {'result':False,'message':u"该球员已经在场上"}
	else:
		return {'result':False,'message':u"球员不存在"}

def SignPlayer(dynamicId,characterId,playerId,gamecoin):#签约球员
	'''签约球员'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	player=gamer.player.getPlayer(playerId)
	if gamer.finance.addGameCoin(-gamecoin):
		player.setPlayerCategory(2)
		player.setPlayerpos('z')
		return {'result':True,'message':u""}
	else:
		return {'result':False,'message':u"银币不足"}



