#coding:utf8
'''
Created on 2014-3-3

@author: CC
'''

from app.game.component.Component import Component
from app.game.component.task.Task import Task
from app.game.core.Item import Item
from app.share.dbopear import dbTask

class CharacterTaskComponent(Component):
	''''''
	
	def __init__(self,owner):
		'''
		Constructor
		'''
		Component.__init__(self,owner)
		self._tasks={}#正在进行的任务
		self._finished=[]#已经完成的任务

	def initCharacterTask(self):
		'''初始化角色任务'''
		characterId=self._owner.baseInfo.id
		processlist=dbTask.getAllProcessInfo(characterId)
		if not processlist:
			return
		for process in processlist:
			taskId=process.get('taskId')
			if process['finished']:
				self._finished.append(taskId)
				continue
			task=Task(taskId,characterId=self._owner.baseInfo.id)
			task.initTaskData(process)
			self._tasks[taskId]=task

	def getExpBound(self,exp):
		'''获取经验奖励'''
		self._owner.level.updateExp(self._owner.level.getExp()+exp)

	def getGamecoinBound(self,gamecoin):
		'''获取银币奖励'''
		self._owner.finance.addGameCoin(gamecoin)

	def getTrainPointBound(self,trainpoint):
		'''获取训练点奖励'''
		self._owner.attribute.setTrainPoint(self._owner.attribute.getTrainPoint()+trainpoint)

	def getReputeBound(self,repute):
		self._owner.attribute.setRepute(self._owner.attribute.getRepute()+repute)

	def getReceivedTaskList(self):
		'''获取已接任务列表'''
		canReceivedTaskList=[]
		for task in self._tasks.values():
			canReceivedTaskList.append(task.formatTaskInfo())
		allTask=dbTask.all_TaskTemplate
		tasklist=allTask.keys()
		for taskId in tasklist:
			if self.canReceived(taskId):
				self.autoApplyTask(taskId)
				taskInfo=Task(taskId,characterId=self._owner.baseInfo.id,status=1)
				canReceivedTaskList.append(taskInfo.formatTaskInfo())

		return {"tasks":canReceivedTaskList}

	def autoApplyTask(self,taskId):
		'''自动接受任务'''
		characterId=self._owner.baseInfo.id
		if not self.canReceived(taskId):
			return {'result':False,'message':u"",'task_id':taskId}
		task=Task(taskId,characterId=characterId)
		result=task.InsertProcess()
		if result:
			self._tasks[taskId]=task

	def canReceived(self,taskId):
		'''判断任务是否可接'''
		allTask=dbTask.all_TaskTemplate
		taskInfo=allTask.get(taskId)
		level=self._owner.level.getLevel()
		if not taskInfo:
			return False
		if taskInfo['taskId'] in self._finished:
			return False
		if taskInfo['taskId'] in self._tasks.keys():
			return False
		if taskInfo['levelrequired']>level:
			return False
		if taskInfo['priorityID']!=0 and taskInfo['priorityID'] not in self._finished:
			return False
		return True

	def commitTask(self,taskId):
		task=self._tasks.get(taskId)
		if not task.hasFinished():
			return {'result':False,'message':u""}
		characterId=self._owner.baseInfo.id
		result=self.taskBoundHandle(taskId)#任务奖励处理
		if not result.get('result'):
			return result
		dbTask.UpdateTaskProcess(characterId,taskId,{'finished':1})
		del self._tasks[taskId]
		self._finished.append(taskId)
		return {'result':True,'message':u""}

	def taskBoundHandle(self,taskId):
		'''任务奖励处理'''
		taskInfo=Task(taskId)
		giveitems=taskInfo.resolveItemPrice()
		package=self._owner.pack._package
		bagCnt=package.findSparePositionNum()
		if len(giveitems)>bagCnt:
			return {'result':False,'message':u""}
		for giveitem in giveitems:
			item=Item(itemTemplateId=giveitem.get('templateId'))
			self._owner.pack.putNewItemInPackage(item)
		exp=taskInfo.format.get('expprice')
		if exp>0:self.getExpBound(exp)
		gamecoin=taskInfo.format.get('gamecoinprice')
		if gamecoin>0:self.getGamecoinBound(gamecoin)
		trainpoint=taskInfo.format.get('trainpointprice')
		if trainpoint>0:self.getTrainPointBound(trainpoint)
		repute=taskInfo.format.get('reputeprice')
		if repute>0:self.getReputeBound(repute)
		return {'result':True}




