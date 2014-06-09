#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from gfirefly.dbentrust.dbpool import dbpool
from MySQLdb.cursors import DictCursor
import datetime

def getUserInfo(uid):
	'''
	@param id:int
	'''
	sql="select * from tb_user_character where id =%d"%(uid)
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchone()
	cursor.close()
	conn.close()
	return result

def checkUserPassword(username,password):
	'''
	@param username:str
	@param password:str
	'''
	sql="select id from `tb_register` where username='%s' and password='%s'"%(username,password)
	conn=dbpool.connection()
	cursor=conn.cursor()
	cursor.execute(sql)
	result=cursor.fetchone()
	cursor.close()
	conn.close()
	pid=0
	if result:
		pid=result[0]
	return pid

def getUserInfoByUsername(username,password):
	'''
	@param username:str
	@param password:str
	'''

	sql="select * from `tb_register` where username='%s' and password='%s'" %(username,password)
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchone()
	cursor.close()
	conn.close()
	return result

def createUserCharacter(uid):
	'''
	@param id:int
	'''
	sql="insert into `tb_user_character` (`id`) values(%d)" %uid
	conn=dbpool.connection()
	cursor=conn.cursor()
	count=cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()
	if count >=1:
		return True
	else:
		return False

def updateUserCharacter(userId,filename,characterId):
	'''
	@param userId
	@param filename:str
	@param characterId:int
	'''
	sql="update `tb_user_character` set %s=%d where id=%d"%(filename,characterId,userId)
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

def InsertUserCharacter(userId,characterId):
	''''''
	sql="update tb_character set userid=%d where `id`=%d"%(userId,characterId)
	conn=dbpool.connection()
	cursor=conn.cursor()
	count=cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()
	if count >-1:
		return True
	else:
		return False

def checkCharacterName(nickname):
	'''
	@param nickname:str
	'''
	sql="select `id` from tb_character where nickname='%s'"%nickname
	conn=dbpool.connection()
	cursor=conn.cursor()
	cursor.execute(sql)
	result=cursor.fetchone()
	cursor.close()
	conn.close()
	if result:
		return False
	return True

def creatNewCharacter(nickname,userId):
	'''
	@param nickname:str
	@param uesrId:int
	@param fieldname:str
	'''
	nowdatetime=str(datetime.datetime.today())
	sql="insert into `tb_character`(userId,nickname,createtime) values ('%d','%s','%s')"%(userId,nickname,nowdatetime)
	sql2="select @@IDENTITY"
	conn=dbpool.connection()
	cursor=conn.cursor()
	count=cursor.execute(sql)
	conn.commit()
	cursor.execute(sql2)
	result=cursor.fetchone()
	cursor.close()
	conn.close()
	if result and count:
		characterId=result[0]
		# InsertUserCharacter(userId,characterId)
		return characterId
	else:
		return 0

def getUserCharacterInfo(characterId):
	'''
	'''
	sql="select town from tb_character where id=%d"%(characterId)
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchone()
	cursor.close()
	conn.close()
	return result

def getCharacterInfoByUserId(userId):
	'''
	'''
	sql="select * from tb_character where userid=%d"%(userId)
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchone()
	cursor.close()
	conn.close()
	return result

def CheckUserInfo(Uid):
	''''''
	sql="Select * from tb_register where username='%s'"%Uid
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchone()
	cursor.close()
	conn.close()
	return result

def creatUserInfo(username,password):
	'''
	'''
	sql="insert into tb_register(username,`password`) values ('%s','%s')"%(username,password)
	conn=dbpool.connection()
	cursor=conn.cursor()
	count=cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()
	if(count>=1):
		return True
	return False
