#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.game.core.GamersManager import GamersManager
from app.share.dbopear import dbItems

def GetCompoundPackage_2109(dynamicId,characterId):
	'''获取合成包裹的信息
	'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	response=gamer.pack.HouQuSuiPianBaoguo()
	return response

def GetOneItemInfo(dynamicId,characterId,itemid):
	'''获取单个物品的详细信息
	'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	response=gamer.pack.getOneItemInfo(itemid)
	return response

def GetCompoundItem(dynamicId,characterId,tempid):
	'''获取当前碎片能合成的物品的信息
	'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	suipianinfo=dbItems.all_ItemTemplate.get(tempid)
	if not suipianinfo:
		return {'result':False,'message':u"合成信息不存在"}
	newtempid=suipianinfo.get('compound',0)
	newiteminfo=dbItems.all_ItemTemplate.get(newtempid)
	if not newtempid:
		return {'result':False,'message':u"该物品不能合成"}
	response={}
	info={}
	info['itemid']=0
	info['icon']=newiteminfo['icon']
	info['itemname']=newiteminfo['name']
	info['itemdesc']=newiteminfo['description']
	info['tempid']=newiteminfo['id']


def CompoundItem(dynamicId,characterId,tempid):
	'''合成物品
	'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	response=gamer.pack.CompoundItem(tempid)
	return response