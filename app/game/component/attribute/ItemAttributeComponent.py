#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.game.component.Component import Component
from app.dbfront.memmode import tb_item_admin

class ItemAttributeComponent(Component):
	'''物品附件属性'''

	def __init__(self,owner,durability=-1,isBound=0,identification=1,strengthen=0,workout=0):
		'''初始化物品附件属性
		@param selfExtraAttributebuteId: []int list 物品自身附加属性
		@param durability: int 物品的耐久度
		'''
		Component.__init__(self,owner)
		self.durability=durability #当前耐久
		self.isBound=isBound

	def getDurability(self):
		'''获取物品的耐久度'''
		return self.durability

	def setDurability(self,durability):
		'''设置物品的耐久度
		@param durability: int 物品的耐久度
		'''
		self.durability=durability

	def updateDurability(self,durability):
		'''更新物品的耐久度
		@param durability: int 物品的耐久度
		'''
		self.setDurability(durability)
		itemmode=tb_item_admin.getObj(self._owner.baseInfo.getId())
		props={'durability':durability}
		itemmode.update_multi(props)

	def updateStrength(self,count):
		'''更新物品的强化
		@param count : int 强化等级
		'''
		if self.strengthen!=count:
			strengthen.strengthen=count
			itemmode=tb_item_admin.getObj(self._owner.baseInfo.getId())
			props={'strengthen':count}
			itemmode.update_multi(props)
			self._owner.updateFJ()