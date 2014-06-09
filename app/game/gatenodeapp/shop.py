#coding:utf8
'''
Created on 2014-2-24

@author: CC
'''

from app.game.gatenodeservice import remoteserviceHandle
from app.game.appinterface import shop
import json

@remoteserviceHandle
def getShopInfo_701(dynamicId,request_proto):
	'''获取商店信息'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	shopCategory=argument.get('shopCategory')
	response=shop.getShopInfo(dynamicId,characterId,shopCategory)
	return json.dumps(response)

@remoteserviceHandle
def buyItem_702(dynamicId,request_proto):
	'''购买物品'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	shopCategory=argument.get('shopCategory')
	itemId=argument.get('itemId')
	buyNum=argument.get('buyNum')
	response=shop.buyItem(dynamicId,characterId,shopCategory,itemId,buyNum)
	return json.dumps(response)