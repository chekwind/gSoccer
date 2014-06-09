#coding:utf8
'''
Created on 2014-2-8

@author: CC
'''

from app.game.gatenodeservice import remoteserviceHandle
import json
from app.game.appinterface import packageInfo

@remoteserviceHandle
def getItemInPackage_201(dynamicId,request_proto):
	'''获取角色的包裹信息'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	response=packageInfo.GetPackageInfo(dynamicId,characterId)
	return json.dumps(response)

@remoteserviceHandle
def useItem_202(dynamicId,request_proto):
	'''使用道具'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	itemId=argument.get('itemId')
	targetId=argument.get('targetId')
	response=packageInfo.UseItem(dynamicId,characterId,itemId,targetId)
	return json.dumps(response)