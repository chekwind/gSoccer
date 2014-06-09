#coding:utf8
'''
Created on 2014-1-20

@author: CC
'''

from firefly.utils.singleton import Singleton

class GuildManager:
	'''公会成员单例管理'''
	__metaclass__=Singleton

	def __init__(self):
		self.g={}#key:公会

	def getpidListBygid(self,gid):
		'''根据公会id获取角色id列表'''
		if self.g.has_key(gid):
			return self.g[gid]
		return []

	def getdtidListBygid(self,gid):
		'''根据公会id获取角色动态id列表'''
		if self.g.has_key(gid):
			return self.g.get(gid)

	def add(self,pid,gid):
		'''把角色加入公会
		@param pid: int 角色动态id
		@param gid: int 公会id
		'''
		if not self.g.has_key(gid):
			self.g[gid]=set([])
		self.g.get(gid).add(pid)#添加角色到公会中

	def delete(self,pid,gid):
		'''把角色从公会中删除
		@param pid: int 角色动态id
		@param gid: int 公会id
		'''
		if self.g.has_key(gid):#有这个公会
			if pid in self.g[gid]:#公会中有这个角色
				self.g[gid].remove(pid)