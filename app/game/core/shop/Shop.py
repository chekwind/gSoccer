#coding:utf8
'''
Created on 2014-2-25

@author: CC
'''

from app.game.core.Item import Item
from app.share.dbopear import dbShop

class Shop:
	'''商店类'''

	def __init__(self,shopcategory):
		'''
		@param shopcategory:int 商店的类型
		'''
		self._shopcategory=shopcategory
		self.shopitems={}
		self.itemList={}
		self.initShopData()

	def initShopData(self):
		'''初始化商店信息'''
		self.itemList=dbShop.getShopInfo(self._shopcategory)
		for _item in self.itemList:
			item=Item(itemTemplateId=_item['templateid'])
			# item.baseInfo.setItemPrice(_item['cost'])
			itemInfo={}
			itemInfo['id']=item.baseInfo.getItemTemplateId()
			itemInfo['item']=item.formatItemInfo()
			itemInfo['promotion']=_item['promotion']
			itemInfo['cost']=_item['cost']
			itemInfo['singlecount']=_item['singlecount']
			itemInfo['allcount']=_item['allcount']
			itemInfo['position']=_item['position']
			self.shopitems[itemInfo['id']]=itemInfo

	def getShopInfo(self):
		'''获取商店信息'''
		items=self.shopitems.values()
		return {'items':items}

	def getShopItemsById(self,itemId):
		'''获取商店物品信息'''
		
		return self.shopitems.get(itemId,None)
