#coding:utf8
'''
Created on 2014-1-20

@author: CC
'''
from firefly.utils.singleton import Singleton

class ChaterManager:
	'''聊天成员单例管理
	@param _chaters:所有的在线成员
	'''
	__metaclass__=Singleton

	def __init__(self):
		self._chaters={}
		self.id={}
		from app.share.dbopear import dbCharacter
		from app.chatServer.core.Chater import Chater
		infos=dbCharacter.getAllInfo()#所有角色信息
		for info in infos:
			id=info['id']#角色id
			name=info['nickname']#角色名称
			dengji=info['level']#角色等级
			jy=info['donttalk']#禁言状态
			self.addChater(Chater(id,charactername=name,level=dengji,donttalk=jy))

	def donttalk(self,id,flg):
		'''设置禁言或者不禁言
		@param id: int 聊天角色id
		@param flg: bool 是否禁言 True:禁言 False:不禁言
		'''

		from app.share.dbopear import dbCharacter

		if flg:#禁言
			chater=self.addChaterByid(id)
			if chater:
				chater.donttalk=1 #设置角色禁言
			result=dbCharacter.updateDontTalk(id,1)
			return result
		else:#不禁言
			chater=self.addChaterByid(id)
			if chater:
				chater.donttalk=0#设置角色不禁言
			result=dbCharacter.updateDontTalk(id,0)
			return result

	def getAlldynamicId(self):
		'''获取所有在线角色的动态id'''
		return self.id.keys()

	def getcharacterIdBydynamicId(self,dynamicId):
		'''根据动态id获取角色聊天类id'''
		return self.id[dynamicId]

	def addChater(self,chater):
		'''添加一个成员到在线聊天成员列表中'''
		if self._chaters.has_key(chater.characterId):
			raise Exception("系统记录冲突")
		self._chaters[chater.characterId]=chater

	def addChaterByid(self,id):
		'''添加角色聊天类，如果有了返回存在角色聊天类'''
		from app.chatServer.core.Chater import Chater
		chater=self._chaters.get(id,None)
		if not chater:
			chater=Chater(id)
			self._chaters[id]=chater
		return chater

	def getChaterByCharacterId(self,characterId):
		'''根据角色的id得到聊天成员'''
		try:
			chater=self._chaters[characterId]
			return chater
		except:
			return None

	def updateOnland(self,id,dynamicId):
		'''设置角色登录
		@param id:int 角色id
		@param dynamicId:int 动态id
		'''
		chater=self._chaters[id]
		chater.island=True
		chater.dynamicId=dynamicId
		self.id[dynamicId]=id #动态id对应角色id

	def updateOurLand(self,id,dynamicId):
		'''设置角色下线
		@param id:int 角色id
		@param dynamicId:int 动态id
		'''
		from app.chatServer.core.GuildManager import GuildManager
		chater=self._chaters[id]
		GuildManager().delete(dynamicId,chater.guildid)
		chater.island=False
		chater.dynamicId=-1
		del self.id[dynamicId]#删除这个动态id与角色id的对应关系


