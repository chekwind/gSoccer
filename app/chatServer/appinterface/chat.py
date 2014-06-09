#coding:utf8
'''
Created on 2014-1-20

@author: CC
'''
from app.chatServer.net.pushObjectNetInterface import pushChatMessage
from app.chatServer.core.ChaterManager import ChaterManager
from app.chatServer.core.ChatRoomManager import ChatRoomManager

from app.share.dbopear import dbShieldWord
from app.chatServer.appinterface.gmhandle import doGmCommand
from app.chatServer.core.GuildManager import GuildManager
from app.chatServer.core.language.Language import Lg

def loginToChatServer(dynamicId,characterId,roomId):
	'''登录聊天服务器
	@param dynamicId:int 客户端的id
	@param characterId:int int角色的id
	'''
	chater=ChaterManager().addChaterByid(characterId)
	if chater:
		ChaterManager().updateOnland(characterId,dynamicId)
		chater.setRoomId(roomId)
		ChatRoomManager().joinRoom(dynamicId,roomId)
	gid=chater.guildid #公会id 没有公会默认0
	dtid=chater.dynamicId
	GuildManager().add(dtid,gid)
	targetList=[]
	targetList.append(dynamicId)
	content=Lg().g(638)
	pushChatMessage(5,-1,Lg().g(128),content,[],targetList)
	return {'result':True,'message':Lg().g(25)}


def sendMessage(dynamicId,characterId,topic,content,linkData,tonickname=None):
	'''发送聊天信息
	@param dynamicId:int 客户端的id
	@param characterId:int 角色的id
	@param topic :int 频道的编号
	@param content:string 发送的消息内容
	@param linkData: dict list 连接信息内容
	'''

	chater=ChaterManager().getChaterByCharacterId(characterId)
	if not chater:
		return {'result':False,'message':Lg().g(639)}
	if topic==7:
		toplayer=ChaterManager().getChaterByCharacterId(characterId)
		if not toplayer:
			return {'result':False,"message":Lg().g(640)}
		else:
			topic=toplayer.baseInfo.id

	targetList=[]
	chaterName=chater.getCharacterName()

	if topic==1:#世界聊天
		idlist=ChaterManager().getAlldynamicId()
		targetList=idlist
	elif topic==2:#当前场景
		roomId=chater.getRoomId()
		targetList=ChatRoomManager().getRoomMember(roomId)
	elif topic==3:#公会
		gid=chater.guildid
		if gid<1:
			return {'result':False,"message":Lg().g(641)}
		else:
			plist=GuildManager().getdtidListBygid(gid)
			if plist:
				targetList=list(plist)

	result=doGmCommand(characterId,content)

	pushChatMessage(topic,characterId,chaterName,dbShieldWord.replaceIllegalChar(content),linkData,targetList)
	return {'result':True}


def sendAnnouncement(msg):
	'''发送系统公告'''
	targetList=[]
	for k in ChaterManager()._chaters:
		targetId=ChaterManager()._chaters[k].dynamicId
		targetList.append(targetId)
	pushChatMessage(7,-1,Lg().g(128),0,msg,[],targetList)

def senGuildCement(msg,targetList=[]):
	'''发送错误提示''' 

	for k in ChaterManager()._chaters:
		targetId=ChaterManager()._chaters[k].dynamicId
		targetList.append(targetId)
	pushChatMessage(7,-1,Lg().g(128),0,msg,[],targetList)

def sendSysInfomation(msg,dynamicId,linkData=[]):
	'''发送系统提示消息
	@param msg: 发送的聊天信息
	@param linkData: 物品的有提示信息
	@param dynamicId:角色动态id
	'''
	targetList=[]
	dynamicId=ChaterManager().getChaterDynamicId
	if dynamicId:
		targetList.append(dynamicId)
	pushChatMessage(5,-1,Lg().g(128),-1,msg,linkData,targetList)

def setLinkData(linkData=[]):
	'''设置一个空的角色链接数据
	@param linkData:[] 连接数据 默认值为[]
	'''
	it={}
	it['id']=0
	it['name']=Lg().g(128)
	it['chatEquipType']=1 #0代表物品 1代表角色
	it['itemQuality']=0
	linkData.append(it)

def setAllChatPlayerDynamicId(targetList):
	'''设置所有在线聊天成员的动态id列表'''
	for k in ChaterManager()._chaters:
		targetId=ChaterManager()._chaters[k].dynamicId
		targetList.append(targetId)

def setGuildPlayerDynamicId(gid,targetList):
	'''设置所在公会中在线聊天成员的动态id列表-根据公会id 有返回值（True or False）
	@param gid: int 公会id
	@param targetList: [] 存储角色动态id
	'''
	rgetList1='' #返回角色Id列表
	if len(rgetList1)>=1:
		for l in rgetList1:
			icno=ChaterManager().getChaterByCharacterId(l)
			if icno:
				targetList.append(icno.dynamicId)
	else:
		return False
	return True
def setToPlayerDynamicId(characterId,targetList):
	'''设置私聊成成员的动态id-根据接收方角色id 有返回值（True or False）
	@param characterId:int 接收方角色id
	'''
	inco=ChaterManager().getChaterByCharacterId(characterId)
	if inco:
		targetList.append(inco.dynamicId)
		return True
	else:
		return False


