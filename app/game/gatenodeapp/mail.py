#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.game.gatenodeservice import remoteserviceHandle
import json
from app.game.appinterface import mail

@remoteserviceHandle
def getMailList_501(dynamicId,request_proto):
	'''获取邮件列表'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	response=mail.getMailList(dynamicId,characterId)
	return json.dumps(response)

@remoteserviceHandle
def sendMail_502(dynamicId,request_proto):
	'''发送邮件'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	gamerName=argument.get('pname')
	title=argument.get('title')
	content=argument.get('content')
	response=mail.sendMail(dynamicId,characterId,gamerName,title,content)
	return json.dumps(response)

@remoteserviceHandle
def getMailInfo_505(dynamicId,request_proto):
	'''获取邮件内容'''
	argument=json.loads(request_proto)
	characterId=argument.get('characterId')
	mailID=argument.get('mailID')
	response=mail.getMailInfo(dynamicId,characterId,mailID)
	return json.dumps(response)