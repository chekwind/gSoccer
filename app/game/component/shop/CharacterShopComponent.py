#coding:utf8
'''
Created on 2014-2-26

@author: CC
'''

from app.game.component.Component import Component
from app.game.core.pack.ShopPackage import ShopPackage
from app.game.core.shop.shopmanager import ShopManager

class CharacterShopComponent(Component):
	'''个人商店类'''

	def __init__(self,owner):
		''''''
		Component.__init__(self,owner)
		self.shopPackage=ShopPackage()

	def buyItem(self,shopCategory,itemTemplateID,buyNum):
		'''购买商店中的物品'''
		shop=ShopManager().getShopByCategory(shopCategory)
		if not shop:
			return {'result':False,'message':u"商店不存在"}
		itemInfo=shop.getShopItemsById(itemTemplateID)
		if not itemInfo:
			return {'result':False,'message':u"道具不存在"}
		SurplusCoin=0
		if shopCategory==1:
			SurplusCoin=self._owner.finance.getCoin()-itemInfo['cost']*buyNum
		else:
			SurplusCoin=self._owner.finance.getGameCoin()-itemInfo['cost']*buyNum
		if SurplusCoin<0:
			return {'result':False,'message':u"金币不足"}
		result=self._owner.pack.putNewItemsInPackage(itemTemplateID,buyNum)
		if not result:
			return {'result':False,'message':u"道具添加失败"}
		if shopCategory==1:
			self._owner.finance.updateCoin(SurplusCoin)
		else:
			self._owner.finance.updateGameCoin(SurplusCoin)
		self._owner.updateGamerDBInfo()
		return {'result':True,'message':u"购买成功"}