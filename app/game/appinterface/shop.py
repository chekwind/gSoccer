#coding:utf8
'''
Created on 2014-2-24

@author: CC
'''

from app.game.core.GamersManager import GamersManager
from app.game.core.shop.shopmanager import ShopManager
from app.game.core.shop.Shop import Shop

def getShopInfo(dynamicId,characterId,shopCategory):
	'''获取商城信息
	@param dynamicId:int 客户端id
	@param characterId:int 角色id
	@param shopCategory:int 商店类型 1金币2银币
	'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	shop=ShopManager().getShopByCategory(shopCategory)
	if not shop:
		shop=Shop(shopCategory)
		ShopManager().addShop(shop)
	data=shop.getShopInfo()
	return {'result':True,'data':data}

def buyItem(dynamicId,characterId,shopCategory,itemId,buyNum):
	'''购买道具'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	data=gamer.shop.buyItem(shopCategory,itemId,buyNum)
	return data