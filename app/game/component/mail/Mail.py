#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.share.dbopear import dbMail

class Mail(object):
	'''
	mail object 邮件
	'''
	def __init__(self,id=0,title='',senderId=-1,receiverId=-1,sender=u'',content=u'',type=1,isReaded=0,isSaved=0,sendTime=u'',gamecoinContains=0,coinContains=0,couponContains=0):
		'''初始化邮件信息
		'''
		self._id=id#邮件的ID
		self._title=title #邮件的主题
		self._senderId=senderId #发送人id
		self._sender=sender #发送者的昵称
		self._receiverId=receiverId #接受人id
		self._type=type #邮件的类型 (1.系统邮件 2.玩家邮件)
		self._content=content #邮件的内容
		self._isReaded=isReaded #是否已读
		self._isSaved=isSaved #是否保存
		self._sendTime=sendTime #发送时间
		self._gamecoinContains=gamecoinContains #邮件中包含的银币
		self._coinContains=coinContains #邮件里包含的金币
		self._couponContains=couponContains #邮件里包含的礼券
		self._mailPackage=None #邮件物品包裹

	def getSenderId(self):
		return self._senderId

	def setSenderId(self,senderId):
		self._senderId=senderId

	def getReceiverId(self):
		return self._receiverId

	def setReceiverId(self,receiverId):
		self._receiverId=receiverId

	def getContent(self):
		return self._content

	def setContent(self,content):
		self._content=content

	def getType(self):
		return self._type

	def setType(self,type):
		self._type=type

	def getIsReaded(self):
		return self._isReaded

	def setIsReaded(self,isReaded):
		self._isReaded=isReaded

	def getIsSaved(self):
		return self._isSaved

	def setIsSaved(self,isSaved):
		self._isSaved=isSaved

	def getSendTime(self):
		return self._sendTime

	def setSendTime(self,sendTime):
		self._sendTime=sendTime

	def getGameCoinContains(self):
		return self._gamecoinContains

	def setGameCoinContains(self,gamecoin):
		self._gamecoinContains=gamecoin

	def getCoinContains(self):
		return self._coinContains

	def setCoinContains(self,coin):
		self._coinContains=coin

	def getCouponContains(self):
		return self._couponContains

	def setCouponContains(self,coupon):
		self._couponContains=coupon

	def formatMainInfo(self):
		'''格式化邮件信息
		'''
		info = dbMail.getMailInfo(self._id)
		data={}
		data['id']=info['id'] #邮件的ID
		data['sender']=info['sender'] #发送者的名称
		data['title']=info['title'] #邮件的标题
		data['sendTime']=str(info['sendTime']) #邮件的发送时间
		data['content']=info['content'] #邮件的内容

		return data

	def mailIntoDB(self):
		'''将邮件写入数据库'''
		result=dbMail.addMail(self._title,self._senderId,self._sender,self._receiverId,self._content,self._type)
		return result

	def updateMainInfo(self,prop):
		'''更新邮件信息'''
		result=dbMail.updateMainInfo(self._id,prop)
		return result

	def destoryMail(self):
		'''销毁邮件'''
		result=dbMail.deleteMail(self._id)
		return result


def sendMail(title,senderId,sender,receiverId,content,type):
	'''发送邮件
	@param senderId:int 发送者的ID，系统发送时为-1
	@param sender:str 发送者的名称，系统发送时为Lg().g(128)
	@param receiverId:int 接受者的ID
	@param content: str 邮件的内容
	@param type:int 邮件的类型 （1，系统邮件 2，玩家邮件）
	'''

	m=Mail(title=title,type=0,senderId=senderId,receiverId=receiverId,sender=u"系统",content=content)
	m.mailIntoDB()