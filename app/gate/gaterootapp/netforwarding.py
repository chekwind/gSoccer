#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from gfirefly.server.globalobject import rootserviceHandle,GlobalObject
from app.gate.gateservice import localservice
from app.gate.core.UsersManager import UsersManager
from app.gate.core.VCharacterManager import VCharacterManager
from app.gate.core.scenesermanger import SceneSerManager
from twisted.python import log

@rootserviceHandle
def forwarding(key,dynamicId,data):
	'''
	'''
	if localservice._targets.has_key(key):
		return localservice.callTarget(key,dynamicId,data)
	else:
		user=UsersManager().getUserByDynamicId(dynamicId)
		if not user:
			return "-1"
		if not user.CheckEffective():
			return "-2"
		oldvcharacter=VCharacterManager().getVCharacterByClientId(dynamicId)
		if not oldvcharacter:
			return
		if oldvcharacter.getLocked():#判断角色对象是否被锁定
			return
		node=VCharacterManager().getNodeByClientId(dynamicId)
		return GlobalObject().root.callChild(node,key,dynamicId,data)

@rootserviceHandle
def pushObject(topicID,msg,sendList):
	'''
	'''
	GlobalObject().root.callChild("net","pushObject",topicID,msg,sendList)

@rootserviceHandle
def opera_gamer(pid,opera_str):
	''''''
	vcharacter=VCharacterManager().getVCharacterByCharacterId(pid)
	if not vcharacter:
		node="game1"
	else:
		node=vcharacter.getNode()
	GlobalObject().root.callChild(node,99,pid,opera_str)

def SaveGamerInfoInDB(dynamicId):
	'''将玩家信息写入数据库'''
	vcharacter=VCharacterManager().getVCharacterByClientId(dynamicId)
	node=vcharacter.getNode()
	result=GlobalObject().root.callChild(node,2,dynamicId)
	return result

def dropClient(deferResult,dynamicId,vcharacter):
	'''清理客户端的记录
	@param result:写入后返回的结果
	'''
	node=vcharacter.getNode()
	if node:#角色在场景中的处理
		SceneSerManager().dropClient(node,dynamicId)
	VCharacterManager().dropVCharacterByClientId(dynamicId)
	UsersManager().dropUserByDynamicId(dynamicId)

@rootserviceHandle
def netconnlost(dynamicId):
	'''客户端断开连接时的处理
	@param dynamicId:int 客户端的动态ID
	'''
	vcharacter=VCharacterManager().getVCharacterByClientId(dynamicId)
	if vcharacter and vcharacter.getNode()>0:#判断是否已经登入角色
		vcharacter.lock()#锁定角色
		result=SaveGamerInfoInDB(dynamicId)#保存角色,写入角色数据
		if result:
			dropClient(result,dynamicId,vcharacter)#清理客户端的数据
	else:
		UsersManager().dropUserByDynamicId(dynamicId)