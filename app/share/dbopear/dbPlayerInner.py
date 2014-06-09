#coding:utf8
'''
Created on 2014-2-15

@author: CC
'''
from gfirefly.dbentrust.dbpool import dbpool
from MySQLdb.cursors import DictCursor
from gfirefly.dbentrust import util

def getByid(characterId):
	'''根据角色id获取寻找球员信息'''
	sql="SELECT * FROM tb_player_inner where characterId=%s"%characterId
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchone()
	cursor.close()
	conn.close()
	if result:
		return result
	return None

def addInfo(characterId,ctime1,ctime2,cs1,cs2,xy,point):
	'''添加记录'''
	sql="insert into `tb_player_inner`(`characterId`,`ctime1`,`ctime2`,`cs1`,`cs2`,`xy`,`point`) values (%d,'%s','%s',%d,%d,%d,%d)"%(characterId,ctime1,ctime2,cs1,cs2,xy,point)
	conn=dbpool.connection()
	cursor=conn.cursor()
	count=cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()
	if count>=1:
		return True
	else:
		return False

def updateInfo(characterId,ctime1,ctime2,cs1,cs2,xy,point):
	'''更改寻找球员记录'''
	sql="update `tb_player_inner` set `ctime1`='%s',`ctime2`='%s',`cs1`=%d,`cs2`=%d,`xy`=%d,`point`=%d WHERE `characterId`=%d"%(ctime1,ctime2,cs1,cs2,xy,point,characterId)
	conn=dbpool.connection()
	cursor=conn.cursor()
	count=cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()
	if count>=1:
		return True
	else:
		return False

