#coding:utf8
'''
Created on 2014-3-3

@author: CC
'''

from app.game.core.GamersManager import GamersManager

def TaskAcceptTaskList(dynamicId,characterId):
	'''获取可接任务列表
	@param dynamicId: int 客户端动态id
	@param characterId: int 角色id
	'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	data=gamer.task.getReceivedTaskList()
	return {'result':True,'data':data}

def commitTask(dynamicId,characterId,taskId):
	'''提交任务'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	gamer.task._tasks.get(taskId).setStatus(1)
	data=gamer.task.commitTask(taskId)
	return data