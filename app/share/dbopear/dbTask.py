#coding:utf8
'''
Created on 2014-3-3

@author: CC
'''
from gfirefly.dbentrust.dbpool import dbpool
from MySQLdb.cursors import DictCursor
from gfirefly.dbentrust import util
import datetime

all_TaskTemplate={}

def getALLTask():
	'''获取所有任务'''
	sql="SELECT * FROM tb_task where enable=1"
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchall()
	cursor.close()
	conn.close()
	for taskInfo in result:
		all_TaskTemplate[taskInfo['taskId']]=taskInfo

def getAllProcessInfo(characterId):
	'''获取所有的在进行中的任务列表'''
	sql="SELECT * FROM tb_task_process WHERE characterId=%d"%characterId
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchall()
	cursor.close()
	conn.close()
	return result

def InsertTaskProcess(characterId,taskId):
	'''添加任务进度信息'''
	sql="INSERT INTO tb_task_process(taskId,characterId) VALUES(%d,%d)"%(taskId,characterId)
	conn=dbpool.connection()
	cursor=conn.cursor()
	count=cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()
	if count:
		return True
	return False

def UpdateTaskProcess(characterId,taskId,props):
	'''更新任务进度'''
	sql=util.forEachUpdateProps('tb_task_process',props,{'characterId':characterId,'taskId':taskId})
	conn=dbpool.connection()
	cursor=conn.cursor()
	count=cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()
	if count:
		return True
	return False










