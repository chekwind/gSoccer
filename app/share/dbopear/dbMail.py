#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from gfirefly.dbentrust.dbpool import dbpool
from MySQLdb.cursors import DictCursor
from gtwisted.utils import log
from gfirefly.dbentrust import util

LEVEL_MAIL={}#所有等级的邮件提示

def forEachQueryProps(sqlstr,props):
	'''遍历所要查询属性，以生成sql语句'''
	if props=='*':
		sqlstr+=' *'
	elif type(props)==type([0]):
		i=0
		for prop in props:
			if(i==0):
				sqlstr+=' '+prop
			else:
				sqlstr+=', '+prop
			i+=1
	else:
		log.msg('props to query must be list')
		return
	return sqlstr

def getAllLevelMail():
	'''获取所有的等级邮件提示
	'''
	global LEVEL_MAIL
	sql="SELECT * FROM tb_levelmail"
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchall()
	cursor.close()
	conn.close()
	sceneInfo={}
	for scene in result:
		sceneInfo[scene['level']]=scene
	LEVEL_MAIL=sceneInfo
	return sceneInfo

def getGamerMailCnd(characterId,mtype):
	'''获取角色邮件列表长度
	@param characterId:int 角色的ID
	@param type:int 邮件的分页类型
	'''
	cnd=0
	if mtype==0:
		cnd=getGamerAllMailCnd(characterId)
	elif mtype==1:
		cnd=geyGamerSysMailCnd(characterId)
	elif mtype==2:
		cnd=getGamerFriMailCnd(characterId)
	elif mtype==3:
		cnd=getGamerSavMailCnd(characterId)
	return cnd

def getGamerAllMailCnd(characterId):
	'''获取玩家所有邮件的数量'''
	sql="SELECT COUNT(`id`) FROM tb_mail WHERE receiverId=%d and isSaved =0"%characterId
	conn=dbpool.connection()
	cursor=conn.cursor()
	cursor.execute(sql)
	result=cursor.fetchone()
	cursor.close()
	conn.close()
	return result[0]

def getGamerFriMailCnd(characterId):
	'''获取角色玩家邮件的数量'''
	sql="SELECT COUNT(id) FROM tb_mail WHERE receiverId=%d and `type`=1 and isSaved=0"%characterId
	conn=dbpool.connection()
	cursor=conn.cursor()
	cursor.execute(sql)
	result=cursor.fetchone()
	cursor.close()
	conn.close()
	return result[0]

def getGamerSysMailCnd(characterId):
	'''获取角色系统邮件数量'''
	sql="SELECT COUNT(id) FROM tb_mail WHERE receiverId=%d and `type`=0 and isSaved=0"%characterId
	conn=dbpool.connection()
	cursor=conn.cursor()
	cursor.execute(sql)
	result=cursor.fetchone()
	cursor.close()
	conn.close()
	return result[0]

def getGamerSavMailCnd(characterId):
	'''获取保存邮件的数量'''
	sql="SELECT COUNT(id) FROM tb_mail where receiverId=%d and `isSaved`=1"%characterId
	conn=dbpool.connection()
	cursor=conn.cursor()
	cursor.execute(sql)
	result=cursor.fetchone()
	cursor.close()
	conn.close()
	return result[0]


def getGamerSysMailList(characterId):
	'''获取角色系统邮件列表
	@param characterId: int 角色的id
	'''
	filedList = ['id','title','type','isReaded','sendTime','content']
	sqlstr=''
	sqlstr=forEachQueryProps(sqlstr,filedList)
	sql="select %s from `tb_mail` where receiverId=%d and `type`=0 and isSaved=0 order by isReaded,sendTime desc"%(sqlstr,characterId)
	conn=dbpool.connection()
	cursor=conn.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	cursor.close()
	conn.close()
	data=[]
	for mail in result:
		mailInfo={}
		for i in range(len(mail)):
			mailInfo[filedList[i]]=mail[i]
		data.append(mailInfo)
	return data

def getGamerFriMailList(characterId):
	'''获取角色好友邮件列表
	@param characterId:int 角色的id
	'''
	filedList=['id','title','type','isReaded','sendTime','content']
	sqlstr=''
	sqlstr=forEachQueryProps(sqlstr,filedList)
	sql="select %s from `tb_mail` where receiverId=%d and `type`=1 and isSaved = 0 order by isReaded"%(sqlstr,characterId)
	conn=dbpool.connection()
	cursor=conn.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	cursor.close()
	conn.close()
	data=[]
	for mail in result:
		mailInfo={}
		for i in range(len(mail)):
			mailInfo[filedList[i]]=mail[i]
		data.append(mailInfo)
	return data

def getGamerSavMailList(characterId):
	'''获取角色保存邮件列表
	@param characterId:int 角色的id
	'''
	filedList=['id','title','type','isReaded','sendTime','content']
	sqlstr=''
	sqlstr=forEachQueryProps(sqlstr,filedList)
	sql="select %s from `tb_mail` where receiverId=%d and `isSaved` =1 order by isReaded LIMIT"%(sqlstr,characterId)
	conn=dbpool.connection()
	cursor=conn.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	cursor.close()
	conn.close()
	data=[]
	for mail in result:
		mailInfo={}
		for i in range(len(mail)):
			mailInfo[filedList[i]]=mail[i]
		data.append(mailInfo)
	return data

def checkMail(mailId,characterId):
	'''检测邮件是否属于characterId
	@param characterId:int 角色的id
	@param mailId:int 邮件的id
	'''
	sql="SELECT `id` from tb_mail WHERE id=%d and receiverId=%d"%(mailId,characterId)
	conn=dbpool.connection()
	cursor=conn.cursor()
	cursor.execute(sql)
	result=cursor.fetchone()
	cursor.close()
	conn.close()
	if result:
		return True
	return False

def updateMailInfo(mailId,prop):
	'''更新邮件信息'''
	sql=util.forEachUpdateProps('tb_mail',prop,{'id':mailId})
	conn=dbpool.connection()
	cursor=conn.cursor()
	count=cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()
	if(count>=1):
		return True
	return False

def addMail(title,senderId,sender,receiverId,content,mailtype):
	'''添加邮件'''
	sql="INSERT INTO tb_mail(title,senderId,sender,receiverId,`type`,content,sendTime) VALUES ('%s',%d,'%s',%d,%d,'%s',CURRENT_TIMESTAMP())"%(title,senderId,sender,receiverId,mailtype,content)
	conn=dbpool.connection()
	cursor=conn.cursor()
	count=cursor.execute(sql)
	conn.commit()
	cursor.close()
	if(count>=1):
		return True
	return False

def deleteMail(mailId):
	'''删除邮件'''
	sql="DELETE FROM tb_mail WHERE id=%d"%mailId
	conn=dbpool.connection()
	cursor=conn.cursor()
	count=cursor.execute(sql)
	conn.commit()
	cursor.close()
	if(count>=1):
		return True
	return False
