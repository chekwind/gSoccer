#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.gate.appinterface import login
import json
from app.gate.gateservice import localserviceHandle

@localserviceHandle
def registerToServer_100(key,dynamicId,request_proto):
	'''账号注册'''
	argument=json.loads(request_proto)
	dynamicId=dynamicId
	username=argument.get('username')
	password=argument.get('password')
	data=login.registerToServer(dynamicId,username,password)
	return json.dumps(data)

@localserviceHandle
def loginToServer_101(key,dynamicId,request_proto):
	'''账号登录'''
	argument=json.loads(request_proto)
	dynamicId=dynamicId
	username=argument.get('username')
	password=argument.get('password')
	data=login.loginToServer(dynamicId,username,password)
	return json.dumps(data)

@localserviceHandle
def createRole_102(key,dynamicId,request_proto):
	'''创建角色'''
	argument=json.loads(request_proto)
	userId=argument.get('userId')
	nickName=argument.get('rolename')
	data=login.createRole(dynamicId,userId,nickName)
	return json.dumps(data)

def SerializePartialEnterScene(result,response):
	'''序列化进入场景的返回消息'''
	return json.dumps(result)

@localserviceHandle
def roleLogin_103(key,dynamicId,request_proto):
	'''角色登陆'''
	argument=json.loads(request_proto)
	userId=argument.get('userId')
	data=login.roleLogin(dynamicId,userId)
	if not data.get('result') or not data.get('data').get('hasRole'):
		return json.dumps(data)
	placeId=data['data'].get('placeId',1000)
	characterId=data['data'].get('characterId',0)
	response=login.enterScene(dynamicId,characterId,placeId,True)
	return json.dumps(response)