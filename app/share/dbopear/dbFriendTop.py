#coding:utf8
'''
Created on 2014-1-21

@author: CC
'''

from gfirefly.dbentrust.dbpool import dbpool
from MySQLdb.cursors import DictCursor

def getReader(characterid):
	'''获取未读信息角色id
	@param characterid: int 角色id
	'''
	sql="SELECT * FROM tb_friend_chat WHERE characterid="+str(characterid)
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	data=cursor.fetchone()
	cursor.close()
	conn.close()
	if not data:
		return None
	return data

def getFriendTop(characterid):
	'''获取最近联系人
	@param characterid:int 当前角色id
	'''
	sql="select friendsid from tb_friend_chat where characterid="+str(characterid)
	conn=dbpool.connection()
	cursor=conn.cursor()
	cursor.execute(sql)
	data=cursor.fetchone()
	cursor.close()
	conn.close()
	if data:
		return eval([data[0]])
	return None

def updateFriendTop(characterid,friendsid,readersid):
	'''修改最近联系人
	@param characterid:int 当前角色id
	@param friendsid:str 最近联系人角色id列表
	@param readersid:str 未读取的信息发送者角色id
	'''
	sql="update tb_friend_chat set friendsid="+friendsid+",reader="+readersid+"where characterid="+str(characterid)
	conn=dbpool.connection()
	cursor=conn.cursor()
	count=cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()
	if count>=1:
		return True
	return False

def addFriendTop(characterid,friendsid):
	'''添加最近联系人
	@param characterid: int 当前角色id
	@param friendsid: str 最近联系人角色id列表
	'''
	sql="insert into `tb_friend_chat`(`characterid`,`friendsid`) values ("+characterid+",'"+friendsid+"')"
	conn=dbpool.connection()
	cursor=conn.cursor()
	count=cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()
	if count>=1:
		return True
	return False