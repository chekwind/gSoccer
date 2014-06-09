#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.game.component.baseInfo.ItemBaseInfoComponent import ItemBaseInfoComponent
from app.game.component.attribute.ItemAttributeComponent import ItemAttributeComponent
from app.game.component.pack.ItemPackComponent import ItemPackComponent
from app.share.dbopear import dbItems
from app.dbfront.memmode import tb_item_admin
import datetime

class Item(object):
	'''物品类'''

	def __init__(self,itemTemplateId=0,id=0,name=''):
		'''初始化物品类
		@param id: int 物品在数据库中的id
		@param itemTemplateId: int 物品的模板id
		@param selfExtraAttributeId: []int list 物品自身的附加属性
		'''
		self.baseInfo=ItemBaseInfoComponent(self,id,name,itemTemplateId)
		self.attribute=ItemAttributeComponent(self)
		self.pack=ItemPackComponent(self)

	def initItemInstance(self,itemInstance):
		'''初始化实际物品信息
		'''
		self.baseInfo.setItemTemplateId(itemInstance['itemTemplateId'])
		self.attribute.setDurability(itemInstance['durability'])
		self.pack.setStack(itemInstance['stack'])

	def getLJtype(self):
		'''获取零件类型'''
		iteminfo=self.baseInfo.getItemTemplateInfo()#物品模板id信息
		typeid=iteminfo.get('bodyType',0)
		return typeid

	def formatItemInfo(self):
		'''格式化物品信息'''
		data=self.baseInfo.getItemTemplateInfo()
		data['id']=self.baseInfo.getId()
		data['templateId']=self.baseInfo.getItemTemplateId()
		data['stack']=self.pack.getStack()
		return data

	def InsertItemIntoDB(self,characterId=0):
		'''将物品信息写入数据库'''
		if self.baseInfo.id:
			return
		itemTemplateId=self.baseInfo.itemTemplateId
		isBound=0
		durability=-1
		stack=self.pack.getStack()
		data={'characterId':characterId,'itemTemplateId':itemTemplateId,'isBound':isBound,'accesstime':datetime.datetime.now(),'durability':durability,'stack':stack}
		newitemmode=tb_item_admin.new(data)
		itemId=int(newitemmode._name.split(':')[1])
		self.baseInfo.setId(itemId)
		return itemId

	def destoryItemInDB(self):
		'''删除数据库中的自身的信息'''
		if self.baseInfo.id!=0:
			return tb_item_admin.deleteMode(self.baseInfo.id)
		return False