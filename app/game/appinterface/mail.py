#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.game.core.GamersManager import GamersManager
from app.share.dbopear import dbShieldWord,dbCharacter

def getMailList(dynamicId,characterId):
	'''获取邮件列表
	@param characterId: int 角色的ID
	'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return{'result':False,'message':u"角色不存在"}
	mailListInfo=gamer.mail.getMailList()
	return {'result':True,'data':mailListInfo}

def getMailInfo(dynamicId,characterId,mailId):
	'''获取邮件的详细信息
	@param characterId: int 角色的ID
	@param mailId: int 邮件的ID
	'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	mailInfo=gamer.mail.readMail(mailID)
	return mailInfo

def SaveAndDeleteMail(dynamicId,characterId,setType,requestInfo,mailId,responseMailType):
	'''删除或保存邮件
	@param characterId:int 角色的ID
	@param setType:int 操作类型 0保存1删除单条数据2删除一页数据
	@requestInfo:int 单条时的邮件ID
	@param mailId: (int) list 批量时邮件的ID列表
	'''
	gamer=GamersManager.getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	if setType==0:
		result=gamer.mail.saveMail(requestInfo)
	elif setType==1:
		result=gamer.mail.deleteMail(requestInfo)
	else:
		result=gamer.mail.BatchDelete(mailId)
	if result['result']:
		pgcnd=gamer.mail.getPageCnd(responseMailType)
		result['data']={}
		result['data']['maxPage']=pgcnd
		result['data']['setTypeResponse']=setType
	return result

def sendMail(dynamicId,characterId,gamerName,title,content):
	'''添加邮件
	@param dynamicId:int 客户端的动态id
	@param characterId:int 角色的ID
	@param gamerName:str 接收人的名称
	@param content:str 邮件内容
	@param title:str 标题
	'''
	gamer=GamersManager().getGamerByID(characterId)
	if not gamer or not gamer.CheckClient(dynamicId):
		return {'result':False,'message':u"角色不存在"}
	if not dbShieldWord.checkIllegalChar(title):
		return {'result':False,'message':u""}
	if not dbShieldWord.checkIllegalChar(content):
		return {'result':False,'message':u""}
	if len(title)>12:
		return {'result':False,'message':u""}
	toId=dbCharacter.getCharacterIdByNickName(gamerName)
	if not toId:
		return {'result':False,'message':u""}
	if toId[0]==characterId:
		return {'result':False,'message':u""}
	result=gamer.mail.sendMail(toId[0],title,content)
	if result:
		return {'result':True,'message':u""}
	return {'result':False,'message':u""}