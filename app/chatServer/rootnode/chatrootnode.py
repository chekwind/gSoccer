#coding:utf8
'''
Created on 2014-1-20

@author: CC
'''

from app.chatServer.core.ChaterManager import ChaterManager
from app.chatServer.core.ChatRoomManager import ChatRoomManager
from app.chatServer.net.pushObjectNetInterface import pushChatMessage

from app.chatServer.protoFile.chat import SystemToInfo2700_pb2
from app.chatServer.core.Lt import Lt
from app.chatServer.core.GuildManager import GuildManager
from app.chatServer.core.language.Language import Lg
from firefly.server.globalobject import GlobalObject,rootserviceHandle

@rootserviceHandle
def JoinRoom(characterId,roomId,scenename):
	'''
	@param characterId: int character id
	@param roomId: int room id
	'''
	chater=ChaterManager().addChaterByid(characterId)
	if not chater:
		return
	clientId=chater.getDynamicId()
	oldroomId=chater.getRoomId()
	chater.setSceneName(scenename)
	if not oldroomId or clientId<0:
		return
	if oldroomId:
		ChatRoomManager().leaveRoom(clientId,oldroomId)
	chater.setRoomId(roomId)
	ChatRoomManager().joinRoom(clientId,roomId)

@rootserviceHandle
def leaveRoom(characterId):
	'''
	@param characterId: int character id
	@param roomId: int room id
	'''
	chater=ChaterManager().getChaterByCharacterId(characterId)
	if not chater:
		return
	clientId=chater.getDynamicId()
	oldroomId=chater.getRoomId()
	if not oldroomId or clientId<0:
		return
	if oldroomId:
		ChatRoomManager().leaveRoom(clientId,oldroomId)

@rootserviceHandle
def updateCharacterLevel(characterId,level):
	'''角色等级同步
	@param characterId: int 角色id
	@param level: int 等级
	'''
	chater=ChaterManager().addChaterByid(characterId)
	chater.level=level

@rootserviceHandle
def updateGuild(characterId,guild,tag):
	'''角色公会同步
	@param characterId: int 角色id
	@param guild: int  公会id
	@param tag:int 1加入 0退出
	'''
	chater=ChaterManager().addChaterByid(characterId)
	if tag==1:
		GuildManager().add(chater.dynamicId,guild)
		chater.guildid=guild
	if tag==0:
		GuildManager().delete(chater.dynamicId,guild)
		chater.guildid=0

@rootserviceHandle
def pushSystemToInfo(strInfo):
	'''推送系统消息'''
	response=SystemToInfo2700_pb2.SystemToInfoResponse()
	try:
		response.s_info=strInfo
	except Exception:
		response.s_info=strInfo.decode('utf8')
	sendList=[chater.getDynamicId() for chater in ChaterManager()._chaters.values()]
	data=response.SerializeToString()
	GlobalObject().netfactory.pushObject(2700,data,sendList)

@rootserviceHandle
def pushSystemchat(strInfo):
	'''推送聊天框系统消息
	@param strInfo: str 系统消息内容
	'''
	sendList=[chater.getDynamicId() for chater in ChaterManager()._chaters.values()]
	pushChatMessage(5,-1,Lg().g(128),0,strInfo,[],sendList)

@rootserviceHandle
def updateDontTalk(characterId,flg):
	'''更新角色禁言状态
	@param characterId:int 角色id
	@param flg:int 0:不禁言 1:禁言
	return 是否成功 True or Flase
	'''
	return ChaterManager().donttalk(characterId,flg)

@rootserviceHandle
def getTalkLog():
	'''获取聊天记录'''
	return Lt().get()