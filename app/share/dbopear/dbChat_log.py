#coding:utf8
'''
Created on 2014-1-21

@author: CC
'''
from gfirefly.dbentrust.dbpool import dbpool
from MySQLdb.cursors import DictCursor

def getChatByid(fid,tid):
	'''获取两人私聊信息
	@param fid:int 其中一人id
	@param tid：int 另一人角色id
	'''
	gdid=0
	if fid>tid:#保证fid比tid小
		gdid=fid
		fid=tid
		tid=gdid

	sql="SELECT * FROM tb_friend_chat_log WHERE fromid="+str(fid)+"AND toid="+str(tid)+"AND (DATE_ADD(times,INTERVAL 24 HOUR)>=CURRENT_TIMESTAMP) ORDER BY times"
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	data=cursor.fetchall()
	cursor.close()
	conn.close()
	if not data:
		return None
	return data

def getCount(fid,tid):
	'''获取聊天条数
	@param fid:int 其中一人id
	@param tid:int 另一个角色id
	'''
	sql="SELECT count(*) FROM tb_friend_chat_log WHERE ((fromid="+str(fid)+" AND toid="+str(tid)+" )OR (fromid="+str(tid)+" AND toid="+str(fid)+")) AND (DATE_ADD(times,INTERVAL 24 HOUR)>=CURRENT_TIMESTAMP) ORDER BY times"
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	data=cursor.fetchall()
	cursor.close()
	conn.close()
	if not data:
		return None
	return data[0]

def delChat(fid,tid):
	'''删除过时信息
	@param fid: int 角色id
	@param tid: int 角色id
	'''
	sql="DELETE FROM tb_friend_chat_log WHERE ((fromid="+fid+" AND toid="+tid+") OR (fromid="+tid+" AND toid="+fid+")) AND (DATE_ADD(times, INTERVAL 24 HOUR)< CURRENT_TIMESTAMP) ORDER BY times"
	conn=dbpool.connection()
	cursor=conn.cursor()
	cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()
	if count:
		return True
	return False

def delAllChat():
	'''删除所有过时信息'''
	sql="DELETE FROM tb_friend_chat_log WHERE DATE_ADD(times,INTERVAL 24 HOUR)< CURRENT_TIMESTAMP"
	conn=dbpool.connection()
	cursor=conn.cursor()
	cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()
	if count:
		return True
	return False