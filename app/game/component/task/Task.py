#coding:utf8
'''
Created on 2014-3-3

@author: CC
'''

from app.share.dbopear import dbTask
from app.game.core.Item import Item

class Task(object):
	'''任务类'''

	def __init__(self,taskId,characterId=0,status=0):
		'''初始化任务信息
		@param taskId:int 
		@param characterId:int 
		@param process: dict
		@param status: int 0未完成 1已完成
		'''
		self._id=taskId
		self.characterId=characterId
		self.process={'killCount':0,'collectCount':0}
		self.format=dbTask.all_TaskTemplate.get(self._id)
		self._status=status

	def initTaskData(self,data):
		'''初始化任务的进度'''
		killCount=data.get('killCount',0)
		collectCount=data.get('collectCount',0)
		self.process={'killCount':killCount,'collectCount':collectCount}

	def getStatus(self):
		'''获取任务状态'''
		return self._status

	def setStatus(self,status):
		'''设置任务状态'''
		self._status=status

	def InsertProcess(self):
		'''写入任务进度'''
		if self.characterId:
			return dbTask.InsertTaskProcess(self.characterId,self._id)
		return False

	def formatTaskInfo(self):
		taskInfo=self.format
		itemBound=self.resolveItemPrice()
		taskInfo['items']=[]
		for item in itemBound:
			taskInfo['items'].append(item)
		return taskInfo

	def resolveItemPrice(self):
		'''解析任务奖励'''
		itemprice=[]
		taskInfo=self.format
		taskprice=eval(taskInfo['itemprice'])
		for prices in taskprice.values():
			for price in prices:
				itemId=price[0]
				stack=price[1]
				item=Item(itemTemplateId=itemId)
				item.pack.setStack(stack)
				itemprice.append({"itemid":itemId,"stack":stack})
		return itemprice

	def hasFinished(self):
		'''查看任务是否完成'''
		taskInfo=self.format
		taskprocess=self.process
		if self._status==1:
			return True
		elif taskInfo.get('monstercount',0)>0:
			if taskprocess['killCount']>=taskInfo['monstercount']:
				self._status=1
				return True
			return False
		elif taskInfo.get('itemcount',0)>0:
			if taskprocess['collectCount']>=taskInfo['itemcount']:
				self._status=1
				return True
			return False
		return False



