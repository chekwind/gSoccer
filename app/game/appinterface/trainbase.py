#coding:utf8
'''
Created on 2014-3-6

@author: CC
'''

from app.game.core.GamersManager import GamersManager
from app.game.core.trainbase.TrainBase import TrainBase
from app.share.dbopear import dbTrainbase
from twisted.internet import reactor
import datetime,time

reactor=reactor

def getTrainBase(dynamicId,characterId):
	'''获取训练基地信息'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	trainbase=TrainBase()
	data=trainbase.getTrainBase()#获取训练基地信息
	return {'result':True,'data':data}

def beginTraining(dynamicId,characterId,num):
	'''开始训练'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	trainpoint=gamer.attribute.getTrainPoint()
	trainbaseinfo=dbTrainbase.getTrainbaseInfo(characterId)#获取训练纪录
	if not trainbaseinfo:
		dbTrainbase.initTrainbaseInfo(characterId)#初始化训练纪录
		trainbaseinfo=dbTrainbase.getTrainbaseInfo(characterId)
	timeleft=trainbaseinfo.get('timeleft')#剩余训练时间
	if not timeleft>0:
		return {'result':False,'message':u"shijianyongjin"}
	startTime=datetime.datetime.now()
	finishTime=startTime+datetime.timedelta(seconds=timeleft)

	trainbase=TrainBase()
	status=trainbase.getTrainBase().get(num).get('status')
	if status==1:#训练场已被占用
		return {'result':False,'message':u"yizhanyong"}

	getTrainPoint=trainbase.getTrainBase().get(num).get('trainpoint')*timeleft/3600
	trainpoint+=getTrainPoint
	dbTrainbase.updateTrainbaseInfo(characterId,{'starttime':str(startTime),'finishtime':str(finishTime),'num':num})#更新训练纪录
	trainbase.setTainBaseStatus(num,1,characterId)#更新训练场为占用
	reactor.callLater(timeleft,doWhenTrainingFinished,{'trainpoint':trainpoint},gamer,num)#训练结束

	return {'result':True,'data':{'startTime':str(startTime),'finishTime':str(finishTime),'gettrainpoint':getTrainPoint}}

def doWhenTrainingFinished(attrs,gamer,num):
	'''训练时间结束'''
	now=datetime.datetime.now()
	trainbaseinfo=dbTrainbase.getTrainbaseInfo(gamer.baseInfo.id)
	finishTime=trainbaseinfo['finishtime']
	if (not finishTime) or (finishTime>now):
		return
	gamer.attribute.setTrainPoint(attrs['trainpoint'])#更新球队训练点
	trainbase=TrainBase()
	trainbase.setTainBaseStatus(num,0)#更新训练场为可用
	dbTrainbase.updateTrainbaseInfo(gamer.baseInfo.id,{'timeleft':0,'num':0})#更新训练纪录

def endTraining(dynamicId,characterId):#中断训练
	'''中断训练'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	trainpoint=gamer.attribute.getTrainPoint()
	trainbaseinfo=dbTrainbase.getTrainbaseInfo(characterId)
	if not trainbaseinfo:
		return {'result':False,'message':u""}
	trainbase=TrainBase()
	now=datetime.datetime.now()
	startTime=trainbaseinfo.get('starttime')
	finishTime=trainbaseinfo.get('finishtime')
	num=trainbaseinfo.get('num')
	if num>0:
		now=int(time.mktime(now.timetuple()))
		startTime=int(time.mktime(startTime.timetuple()))
		finishTime=int(time.mktime(finishTime.timetuple()))
		traintime=now-startTime
		timeleft=finishTime-now
		if timeleft>0:
			getTrainPoint=trainbase.getTrainBase().get(num).get('trainpoint')*traintime/3600
			trainpoint+=getTrainPoint
			dbTrainbase.updateTrainbaseInfo(characterId,{'finishtime':datetime.datetime.now(),'num':0,'timeleft':timeleft})#更新训练纪录
			gamer.attribute.setTrainPoint(trainpoint)#更新球队训练点
			trainbase.setTainBaseStatus(num,0)#更新训练场为可用
			return {'result':True,'data':{'gettrainpoint':getTrainPoint}}
		else:
			return {'result':False,'message':u"xunlianyijieshu"}
	else:
		return {'result':False,'message':u"weixunlian"}






