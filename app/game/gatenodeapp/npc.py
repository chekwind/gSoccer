#coding:utf8
'''
Created on 2014-3-18

@author: CC
'''

from app.game.gatenodeservice import remoteserviceHandle
import json
from app.game.appinterface import npcinfo

@remoteserviceHandle
def getNPCInfo_1301(dynamicId,request_proto):
	'''获取NPC信息'''
	argument=json.loads(request_proto)
	npcid=argument.get('npcid')
	response=npcinfo.GetNPCInfo(dynamicId,npcid)
	return json.dumps(response)

# @remoteserviceHandle
# def getNPCInfo_1302(dynamicId,request_proto):
# 	'''获取NPC实力'''
# 	argument=json.loads(request_proto)
# 	npcid=argument.get('npcid')
# 	response=npcinfo.GetNPCPower(dynamicId,npcid)
# 	return json.dumps(response)