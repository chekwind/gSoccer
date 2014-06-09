#coding:utf8
'''
Created on 2014-3-3

@author: CC
'''

from app.game.gatenodeservice import remoteserviceHandle
from app.game.appinterface import task
import json

@remoteserviceHandle
def AcceptTaskList_801(dynamicId,request_proto):
	'''角色可接的任务列表'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	response=task.TaskAcceptTaskList(dynamicId,characterId)
	return json.dumps(response)

@remoteserviceHandle
def commitTask_802(dynamicId,request_proto):
	'''提交任务'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	taskId=argument.get('taskId')
	response=task.commitTask(dynamicId,characterId,taskId)
	return json.dumps(response)