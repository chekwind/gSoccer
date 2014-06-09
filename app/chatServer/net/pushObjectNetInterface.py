#coding:utf8
'''
Created on 2014-1-20

@author: CC
'''


from app.chatServer.core.language.Language import Lg
from firefly.server.globalobject import GlobalObject
import json

def pushSystemToInfo2700(str,sendList):
	'''推送跑马灯'''
	response['s_info']=str
	pushApplyMessage(2700,json.dumps(response),sendList)

def pushApplyMessage(topic,msg,sendList):
	'''推送消息'''
	GlobalObject().netfactory.pushObject(topic,msg,sendList)

def pushChatMessage(topic,characterId,fromName,content,linkData,sendList):
	'''推送聊天消息
	@param topic: int 聊天频道id 1世界 2当前 3公会 4GM 5系统公告 6公会通告 7错误提示
	@param characterId:int 角色的id (系统 -1)
	@param fromName: str 发送者名称
	@param content: str 聊天的文字内容
	@param sendList: list [int] 发送的客户端id列表
	'''
	response={}
	response['topic']=topic
	response['id']=characterId
	response['fromName']=fromName
	response['linkData']={}
	for _item in linkData:
		item=response['linkData']
		item['chatEquipType']=_item['chatEquipType']
		item['id']=_item['id']
		item['name']=_item['name']
		if _item.has_key('itemInfo'):
			pass
	try:
		response['content']=content
	except Exception:
		response['content']=content.decode('gbk')

	GlobalObject().netfactory.pushObject(1002,json.dumps(response),sendList)

def pushChatToObjectList(id,tid):
	'''推送私聊角色列表'''
	from app.chatServer.core.ChaterManager import ChaterManager
	from app.chatServer.core.ChaterLogManager import ChaterLogManager
	response=ChatToObjectListInfo1010_pb2.ChatToObjectListResponse()
	clog=ChaterLogManager().addChatLog(id)#获取聊天类
	listid=clog.getFriends()#获取角色私聊对象id列表
	if len(listid)<0:
		return
	gamer=ChaterManager().getChaterByCharacterId(id)
	if not gamer:
		return
	gamerid=gamer.getDynamicId()
	for cid in listid:
		gamer1=ChaterManager().getChaterByCharacterId(cid)
		info=response.chatObjectInfo.add()
		info.chatObjectId=cid
		info.name=gamer1.getCharacterName()
		info.level=str(gamer1.level)
		if gamer1.island:
			info.chatObjectPos=gamer1.scenename
		else:
			info.chatObjectPos=lg().g(106)
		info.readFlag=ChaterLogManager().getFriendReaderState(id,cid)
	msg=response.SerializeToString()
	pushApplyMessage(1010,msg,[gamer1])

def pushServerSendChatInfo(id,message,tid):
	'''推送的私聊信息
	@param id: int 私聊对象角色id
	@param tid: int 私聊对象角色id
	@param message: str 聊天内容
	'''
	from app.chatServer.core.ChaterManager import ChaterManager
	response['id']=tid
	response['chatMessage']=message
	chater=ChaterManager().getChaterByCharacterId(id)#推送给这个人的角色
	dyid=chater.dynamicId
	pushApplyMessage(1012,json.dumps(response),[dyid])

def pushOtherMessage(orderId,msg,sendList):
	'''推送其他提示信息'''
	try:
		request['msg']=msg
	except Exception:
		request['msg']=unicode(msg,'gbk')
	pushApplyMessage(905,json.dumps(request),sendList)