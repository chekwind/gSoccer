#coding:utf8
'''
Created on 2014-3-6

@author: CC
'''
from app.game.gatenodeservice import remoteserviceHandle
from app.game.appinterface import trainbase
import json

@remoteserviceHandle
def getTrainBase_1001(dynamicId,request_proto):
	'''获得训练基地信息'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	response=trainbase.getTrainBase(dynamicId,characterId)
	return json.dumps(response)

@remoteserviceHandle
def beginTraining_1002(dynamicId,request_proto):
	'''开始训练'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	num=argument.get('num')
	response=trainbase.beginTraining(dynamicId,characterId,num)
	return json.dumps(response)

@remoteserviceHandle
def endTraining_1003(dynamicId,request_proto):
	'''结束训练'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	response=trainbase.endTraining(dynamicId,characterId)
	return json.dumps(response)