#coding:utf8
'''
Created on 2014-2-7

@author: CC
'''
from app.game.component.Component import Component
from app.game.core.character.Player import Player
import random
from app.dbfront.memmode import tb_player_admin
from app.share.dbopear import dbPlayer

class PlayerComponent(Component):
	'''球队的球员信息类'''
	def __init__(self,owner):
		Component.__init__(self,owner)
		self._players={}#球队的球员列表
		self.lastRemove=[]#最后解雇的球员ID

	def initPlayerInfo(self):
		'''初始化球员信息'''
		cid=self._owner.baseInfo.id
		playerlist=tb_player_admin.getAllPkByFk(cid)
		playerobjlist=tb_player_admin.getObjList(playerlist)
		for playermmode in playerobjlist:
			playerid=int(playermmode._name.split(':')[1])
			player=Player(playerId=playerid)
			PlayerInfo=playermmode.get('data')
			player.initPlayerInstance(PlayerInfo)
			self._players[playerid]=player

	def getPlayers(self):
		'''获取球队的球员列表'''
		return self._players

	def getHasPlayerTemplatrlist(self):
		'''获取已经获得的球员的模板列表'''
		return [player.templateId for player in self._players.values()]

	def formatPlayerListInfo(self):
		'''格式化球队的球员信息'''
		players=self.getPlayers()
		return players.values

	def FormatPlayerList(self):
		'''格式化所有球员的信息'''
		playerinfolist=[]
		players=self.getPlayers()
		for player in players.values():
			playerid=player.baseInfo.getId()
			info=player.formatPlayerInfo()
			playerinfolist.append(info)
		return {'playerlist':sorted(playerinfolist,key=lambda x:x["id"])}

	def getPlayerListInfo(self):
		'''获取球队球员列表'''
		players=self.getPlayers()
		PlayerListInfo={}
		PlayerListInfo['curPlayerNum']=len(players)
		PlayerListInfo['playerInfo']=[]
		for player in players.values():
			info={}
			playerId=player.baseInfo.getId()
			info['playerId']=playerId
			info['PlayerName']=player.baseInfo.getName()
			info['playerLevel']=player.level.getLevel()
			info['PlayerQuality']=player.level.getPlayerQuality()
			PlayerListInfo['playerInfo'].append(info)
		return PlayerListInfo

	def getPlayersListByCategory(self,PlayerCategory=1):
		'''根据球员类型获取球员列表'''
		PlayerListInfo=[]
		players=self.getPlayers()
		for player in players.values():
			info={}
			if player.PlayerCategory==PlayerCategory:
				playerId=player.baseInfo.getId()
				info['playerId']=playerId
				info['PlayerName']=player.baseInfo.getName()
				info['Photo']=player.templateInfo.get('Photo')
				info['PlayerQuality']=player.level.getPlayerQuality()
				info['Role']=player.templateInfo.get('Role')
				PlayerListInfo.append(info)
		return PlayerListInfo


	def getPlayerNum(self,PlayerCategory=1):
		'''获取当前球员的数量'''
		info={}
		players=self.getPlayers()
		for player in players.values():
			if player.PlayerCategory==PlayerCategory:
				info[player.baseInfo.getId()]=player
		return len(info)

	def addPlayer(self,templateId,level=1,PlayerCategory=2,PlayerPos='z'):
		'''添加一个球员'''
		if self.getPlayerNum(2)>8:
			return -1#替补球员已满
		if self.getPlayerNum(3)>8:
			return -2#球员大厅已满
		player=Player(templateId=templateId,level=level,PlayerCategory=PlayerCategory,owner=self._owner.baseInfo.id,PlayerPos=PlayerPos)
		result=player.InsertIntoDB()
		if result:
			self._players[player.baseInfo.getId()]=player
			return player

	def DropPlayer(self,playerId):
		'''解雇球员
		@param playerId:int 球员的id
		'''
		if playerId not in self._players.keys():
			return -5#不存在该球员
		player=self._players.get(playerId)
		result=player.destoryByDB()
		if result:
			del self._players[playerId]
			return 1
		return 0

	def addLastRemove(self,playerId):
		'''添加球员解雇列表'''
		self.lastRemove.append(playerId)

	def popLastRemove(self):
		removelist=list(self.lastRemove)
		self.lastRemove=[]
		return removelist

	def getPlayer(self,playerId):
		'''获取指定的球员'''
		return self._players.get(playerId)

	def PlayerTraining(self,playerId,Shoot,Dribbling,Speed,Pass,Tackle,Tackling,_Save,Response,Trainpoint,gamer):
		'''球员训练'''
		if playerId not in self._players.keys():
			return -5#不存在该球员
		player=self._players.get(playerId)
		result=player.PlayerTraining(Shoot,Dribbling,Speed,Pass,Tackle,Tackling,_Save,Response,Trainpoint,gamer)
		if result:
			player.SavePlayerAttribute()
			gamer.CalPower()
			return {'result':True,'message':u'保存成功'}
		return {'result':False,'message':u'保存失败'}

	def addPlayerExp(self,playerId,exp):
		'''球员加经验'''
		if playerId not in self._players.keys():
			return -5#不存在该球员
		player=self._players.get(playerId)
		result=player.addPlayerExp(exp)
		if result:
			return {'result':True,'message':player.level.getExp()}
		return {'result':False,'message':''}

	def upgradePlayer(self,playerId):
		'''球员升级'''
		if playerId not in self._players.keys():
			return -5#不存在该球员
		player=self._players.get(playerId)
		result=player.upgradePlayer()
		if result:
			return {'result':True,'message':u'升级成功'}

	def IsOnCourt(self,templateId,playerid):
		'''判断是否有同名球员在场上'''
		for player in self._players.values():
			if templateId==player.templateInfo.get('id') and  player.getPlayerpos()!='z' and player.baseInfo.getId()!=playerid:
				return 1
		return 0

	def initBeginPlayer(self):
		'''初始化初始球员'''
		for playertemp in dbPlayer.PLAYER_TEMPLATE_BEGIN.values():
			self.addPlayer(playertemp['id'],1,1,playertemp['PlayerPos'])
		






