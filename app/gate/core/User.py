#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.share.dbopear import dbuser,dbShieldWord,dbclub

INITTOWN=1000

class User:
	'''用户类'''
	def __init__(self,name=0,password=0,dynamicId=-1,uid=0):
		'''
		@param id:int 用户的id
		@param name:str 用户的名称
		@param password:str 用户的密码
		@param pid:int 邀请者的id
		@param dynamicId:str 登录时客户端的动态ID
		@param characterId:dict 用户的角色
		@param isEffective:bool 是否是有效的
		'''
		self.id=uid
		self.name=name
		self.password=password
		self.pid=0
		self.dynamicId=dynamicId
		self.isEffective=True
		self.characterId=0
		self.characterInfo={}
		self.initUser(self.id)

	def initUser(self,userId):
		'''初始化用户类'''
		if userId:
			data=dbuser.getCharacterInfoByUserId(userId)
			if not data:
				self.isEffective=False
				return
			self.characterId=data.get('id',0)
		else:
			data=dbuser.getUserInfoByUsername(self.name,self.password)
			if not data:
				self.isEffective=False
				return
			if not data['enable']:
				self.isEffective=False
			self.id=data.get('id',0)
			self.pid=data.get('pid',0)	

	def getNickName(self):
		'''获取账号名'''
		return self.name

	def CheckEffective(self):
		'''检测账号是否有效'''
		return self.isEffective

	def checkClient(self,dynamicId):
		'''检测客户端ID是否匹配'''
		return self.dynamicId==dynamicId

	def getUserCharacterInfo(self):
		'''获取角色信息'''
		info={}
		info['userId']=self.id
		return info

	def getCharacterInfo(self):
		'''获取角色的信息'''
		if not self.characterInfo:
			self.characterInfo=dbuser.getUserCharacterInfo(self.characterId)
		return self.characterInfo

	def setDynamicId(self,dynamicId):
		'''设置动态ID
		@param dynamicId:int 客户端动态ID
		'''
		self.dynamicId=dynamicId

	def getDynamicId(self):
		'''获取用户动态ID'''
		return self.dynamicId

	def creatNewCharacter(self,nickname):
		'''创建新角色
		@profession (int)
		'''
		if len(nickname)<2 or len(nickname)>20:
			return {'result':False,'message':u'球队不合格'}
		if not dbShieldWord.checkIllegalChar(nickname):
			return {'result':False,'message':u'球队名违法'}
		if self.characterId:
			return {'return':False,'message':u'已经创建过角色'}
		if not dbuser.checkCharacterName(nickname):
			return {'result':False,'message':u'球队名存在'}
		characterId=dbuser.creatNewCharacter(nickname,self.id)
		if characterId:
			self.characterId=characterId
			data={}
			data['userId']=self.id
			data['newCharacterId']=characterId
			cinfo={'id':characterId,'level':1,'nickname':nickname}
			return {'result':True,'message':u'创建角色成功','data':data}
		else:
			return {'result':False,'message':u'创建角色失败'}

	def disconnectClient(self):
		'''断开'''
		from app.gate.gaterootapp.netforwarding import SaveGamerInfoInDB
		dynamicId=self.dynamicId
		SaveGamerInfoInDB(dynamicId)
		self.isEffective=False