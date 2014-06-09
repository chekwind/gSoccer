#coding:utf8
'''
Created on 2014-1-20

@author: CC
'''
from app.share.dbopear import dbCharacter
from app.chatServer.core.language.Language import Lg
ROOMNAME={1000:u''}

class Chater:
	'''
	聊天成员类
	'''
	def __init__(self,characterId,dynamicId=-1,charactername=u'',level=0,donttalk=0):
		'''聊天成员类初始化
		@param characterId: int 角色的id
		@param charactername: str 角色的名称
		@param dynamicId:int 聊天客户端的ID
		@param roomId:int 房间号ID
		'''
		self.charactername=charactername #角色名称
		self.level=level #角色等级
		self.guildid=0 #公会id
		self.dynamicId=dynamicId #角色动态id
		self.island=True #是否在线 False表示离线 True表示在线
		self.characterId=characterId #角色id

		self.scenename=Lg().g(106)#所在场景名称
		self.roomId=0#房间号码
		self.donttalk=donttalk#0不禁言 1禁言
		gid=0#dbGuild.getGuildidBypid(characterId)#通过角色id获取所属公会
		if gid:
			self.guildid=gid
		if len(charactername)<1:
			info.dbCharacter.getInfoByid(characterId)#通过角色id获取角色信息
			if not info:
				print characterId
			self.charactername=info.get('nickname',charactername)#角色名称
			self.level=info.get('level',level)#角色等级
			self.donttalk=info.get('donttalk',0)#0不禁言 1禁言

	def getDynamicId(self):
		'''获取聊天的动态ID'''
		return self.dynamicId

	def getCharacterId(self):
		'''获取聊天成员的ID'''
		return self.characterId

	def getCharacterName(self):
		'''获取聊天成员的名称'''
		return self.charactername

	def setSceneName(self,scenename):
		'''设置场景名称'''
		self.scenename=scenename

	def getSceneName(self):
		'''获取聊天成员躲在的场景的名称'''
		return self.scenename

	def setRoomId(self,roomId):
		'''设置房间id'''
		self.roomId=roomId

	def getRoomId(self):
		'''获取房间ID'''
		return self.roomId
