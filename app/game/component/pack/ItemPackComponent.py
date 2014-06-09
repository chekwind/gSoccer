#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.game.component.Component import Component
from app.dbfront.memmode import tb_item_admin

class ItemPackComponent(Component):
	'''物品在包裹里的组件属性
	pack component for item
	'''

	def __init__(self,owner,idInPack=0,stack=1):
		'''
		Constructor
		'''
		Component.__init__(self,owner)
		self._idInpack=idInPack #物品在包裹里的id
		self._stack=stack #可叠加数:'-1:不可叠加 1~999:可叠加的数值

	def getPosition(self):
		'''获取物品在包裹中的位置'''

	def getIdInPack(self):
		'''获取物品在包裹中的id'''
		return self._idInpack

	def setIdInPack(self,idInPack):
		'''设置物品在包裹中的id'''
		self._idInPack=idInPack

	def getStack(self):
		return self._stack

	def setStack(self,stack):
		self._stack =stack

	def updateStack(self,stack,tag=0):
		'''更新物品的层叠数'''
		self._stack=stack
		if stack>0:
			itemmode=tb_item_admin.getObj(self._owner.baseInfo.id)
			props={'stack':self._stack}
			itemmode.update_multi(props)
		else:
			if tag==0:
				stack._owner.destoryItemInDB()