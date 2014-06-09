#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from gfirefly.utils.singleton import Singleton

class GamersManager:
	'''在线角色单例管理器'''

	__metaclass__=Singleton

	def __init__(self):
		'''初始化单例管理器'''
		self._gamers={}

	def getAll(self):
		alllist=self._gamers.values()
		return alllist

	def addGamer(self,gamer):
		'''添加一个在线角色'''
		if self._gamers.has_key(gamer.baseInfo.id):
			pass
		self._gamers[gamer.baseInfo.id]=gamer

	def getGamerByID(self,cid):
		'''根据角色id获取玩家角色实例
		@id (int) 角色id
		'''
		return self._gamers.get(cid,None)

	def getGamerBydynamicId(self,dynamicId):
		'''根据角色动态id获取玩家角色实例
		@param dynamicId (int) 角色动态id
		'''
		for gamer in self._gamers.values():
			if gamer.dynamicId==dynamicId:
				return gamer
		return None

	def getGamerByNickname(self,nickname):
		'''根据角色昵称获取玩家角色实例
		@nickname (str) 角色昵称
		'''
		for k in self._gamers.values():
			if k.baseInfo.getNickName()==nickname:
				return k
		return None

	def dropGamer(self,gamer):
		'''移除在线角色
		@gamer (GamerCharacter) 角色实例
		'''
		gamerId=gamer.baseInfo.id
		self.dropGamerByID(gamer)

	def dropGamerByID(self,cid):
		'''移除在线角色
		@id (int) 角色id
		'''
		try:
			del self._gamers[cid]
		except:
			pass

	def IsGamerOnline(self,cid):
		'''判断角色是否在线'''
		return self._gamers.has_key(cid)

	def doGamerOffLine(self,gamer):
		'''
		'''
		pass
