#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.game.component.baseInfo.BaseInfoComponent import BaseInfoComponent

class CharacterBaseInfoComponent(BaseInfoComponent):
	'''玩家基础信息组件类'''
	def __init__(self,owner,cid,nickName=u"",viptype=1):
		'''
		Constructor
		'''
		BaseInfoComponent.__init__(self,owner,cid,nickName)
		self._viptype=viptype #玩家类型

	#----------------------nickName-------------------

	def setnickName(self,nickName): #从数据库中读取后赋值
		self._baseName=nickName

	def getNickName(self):#h获取内存中的值
		return self._baseName

	def setType(self,viptype):
		'''设置VIP类型'''
		self._viptype=viptype

	def getType(self):
		'''获取VIP类型'''
		return self._viptype