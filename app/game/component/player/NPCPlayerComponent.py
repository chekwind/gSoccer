#coding:utf8
'''
Created on 2014-3-18

@author: CC
'''
from app.game.component.Component import Component
from app.game.core.character.Player import Player
import random
from app.dbfront.memmode import tb_player_admin

class NPCPlayerComponent(Component):
	'''球队的球员信息类'''
	def __init__(self,owner):
		Component.__init__(self,owner)
		self._players={}#球队的球员列表
		self.lastRemove=[]#最后解雇的球员ID

	def initPlayerInfo(self,cid):
		'''初始化球员信息'''
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
		return {'playerlist':playerinfolist}

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









