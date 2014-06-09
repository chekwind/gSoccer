#coding:utf8
'''
Created on 2014-1-20

@author: CC
'''
from app.chatServer.appinterface import chat
from app.chatServer.core.Lt import Lt
from app.chatServer.core.language.Language import Lg
from firefly.server.globalobject import netserviceHandle
import json

@netserviceHandle
def loginToChatServer_1001(_conn,request_proto):
	'''登录聊天服务器'''
	argument=json.loads(request_proto)
	dynamicId=_conn.transport.sessionno
	characterId=argument.get('characterId')
	roomId=argument.get('roomId')
	data=chat.loginToChatServer(dynamicId,characterId,roomId)
	return json.dumps(data)

@netserviceHandle
def sendMessage_1003(_conn,request_proto):
	'''发送聊天信息'''
	from app.chatServer.core.ChaterManager import ChaterManager
	argument=json.loads(request_proto)
	dynamicId=_conn.transport.sessionno
	characterId=argument.get('characterId')#当前角色id
	topic=argument.get('topic')#频道号
	tonickname=argument.get('tonickname') #角色昵称
	content=argument.get('content') #内容

	chater=ChaterManager().getChaterByCharacterId(characterId)
	if chater.donttalk==0:#不禁言
		linkData=[] #聊天连接信息
		Lt().add(characterId,tonickname,content)
		data=chat.sendMessage(dynamicId,characterId,topic,content,linkData,tonickname)
	else:#禁言
		data={'result':False,"message":Lg().g(644)}
	return json.dumps(data)
