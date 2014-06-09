#coding:utf8
'''
Created on 2014-3-10

@author: CC
'''

from gfirefly.dbentrust.dbpool import dbpool
from MySQLdb.cursors import DictCursor
from gfirefly.dbentrust import util

def getTrainbaseInfo(characterId):
	'''获取玩家训练基地信息'''
	sql="SELECT * FROM tb_character_trainbase where characterId=%s"%characterId
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchone()
	cursor.close()
	conn.close()
	return result

def updateTrainbaseInfo(characterId,props):
	'''修改玩家训练基地纪录'''
	sql=util.forEachUpdateProps('tb_character_trainbase',props,{'characterId':characterId})
	conn=dbpool.connection()
	cursor=conn.cursor()
	count=cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()
	if count:
		return True
	return False

def initTrainbaseInfo(characterId):
	'''初始化玩家训练基地信息'''
	sql="INSERT INTO `tb_character_trainbase`(characterId) VALUES (%d)"%characterId
	conn=dbpool.connection()
	cursor=conn.cursor()
	count=cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()
	if count:
		return True
	return False