#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.game.gatenodeservice import remoteserviceHandle
from app.game.appinterface import roleinfo,player
import json

@remoteserviceHandle
def RoleInfo_105(dynamic,request_proto):
	'''获取角色的状态栏信息
	'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	response=roleinfo.roleInfo(dynamic,characterId)
	return json.dumps(response)

@remoteserviceHandle
def calPower_106(dynamic,request_proto):
	'''计算球队实力'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	response=roleinfo.calPower(dynamic,characterId)
	return json.dumps(response)


