#coding:utf8
'''
Created on 2014-1-21

@author: CC
'''
from firefly.utils.singleton import Singleton
from app.share.dbopear import dbChat_log

class ChatContextManager(object):
	'''聊天内容管理者'''
	__metaclass__=Singleton

	def __init__(self):
		self.contextList={}#所有私聊聊天记录
		self.count=25#两角色聊天文字条数上限
		self.chatList={}#角色发送的聊天信息

	def delchatList(self,fid):
		'''删除担任发送的私聊信息
		@param fid:int 发送聊天角色id
		'''
		if self.chatList.has_key(fid):#如果有记录
			del self.chatList[fid][0]#删除第一条发送的记录

	def addchatList(self,fid,tid,context,time):
		'''添加单人发送的私聊信息
		@param fid:int 发送聊天角色id
		@param tid:int 接受内容角色id
		@param context: str 聊天内容
		@param time: str 时间
		'''
		val={}
		val["fid"]=fid
		val["yid"]=tid
		val["context"]=context
		val["time"]=time
		if not self.chatList.has_key(fid):#没有此人发送信息的记录
			tlist=[]
			tlist.append(val)
			self.chatList[fid]=tlist
		else:#有此人发送聊天信息的记录
			tlist=self.chatList[fid]
			tlist.append(val)

	def getContext(self,fid,tid):
		'''获取双人私聊记录
		@param fid:int 发送聊天角色id
		@param tid:int 接收聊天角色id
		'''
		ke=self.getkey(fid,tid)
		val=u""
		if self.contextList.has_key(ke):#两人私聊过
			for item in self.contextList[ke]:
				val+=item["context"]
		return val

	def addContext(self,fid,tid,context,time):
		'''添加双人互相私聊
		@param fid: int 发送聊天角色id
		@param tid: int 接收聊天角色id
		@param context:str 聊天内容
		@param time: str 时间
		'''
		ke=self.getkey(fid,tid)
		val={}
		val["fid"]=fid
		val["tid"]=tid
		val["context"]=context
		val["time"]=time
		if not self.contextList.has_key(ke):#两人没有私聊过
			tlist=[]
			tlist.append(val)
			self.contextList[ke]=tlist
		else:#私聊过
			tlist=self.contextList[ke]
			tlist.append(val)
			if len(tlist)>self.count:#如果聊天数量超过限制
				del tlist[0]#删除最早的一条双人聊天记录

	def getkey(self,fid,tid):
		'''获取key值
		@param fid:int 发送聊天角色id
		@param tid:int 接收聊天角色id
		'''
		ky=""
		if fid<tid:
			ky=str(fid)+"#"+str(tid)
		else:
			ky=str(tid)+"#"+str(fid)
		return ky
