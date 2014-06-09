#coding:utf8
'''
Created on 2014-2-19

@author: CC
'''
from app.game.component.Component import Component
from app.share.dbopear import dbZen
from app.dbfront.memmode import tb_zen_admin



class CharacterZenComponent(Component):
	'''角色战术组件'''

	def __init__(self,owner):
		'''初始化'''
		Component.__init__(self,owner)
		self._zeninfo={}
		self.initZenInfo()
		self._zenid=1

	def initZenInfo(self):
		'''初始化战术信息'''
		characterId=self._owner.baseInfo.id
		zenmmode=tb_zen_admin.getObj(characterId)
		if not zenmmode:
			self._zeninfo={'characterId':characterId,'zenId':1,'lvzen1':0,'lvzen2':0,'lvzen3':0,'lvzen4':0,'lvzen5':0,'lvzen6':0}
			tb_zen_admin.new(self._zeninfo)
		else:
			self._zeninfo=zenmmode.get("data")

	def getZenInfo(self):
		'''获取战术信息'''
		return self._zeninfo

	def getZenId(self):
		'''获取战术ID'''
		return self._zenid

	def setZenId(self,zenId):
		'''设置战术ID'''
		self._zenid=zenId


	def setZenInfo(self,key,value):
		'''设置战术信息'''
		self._zeninfo[key]=value

	def updateZenInfo(self):
		'''更新战术信息'''
		zenId=self._zenid
		lvzen1=self._zeninfo['lvzen1']
		lvzen2=self._zeninfo['lvzen2']
		lvzen3=self._zeninfo['lvzen3']
		lvzen4=self._zeninfo['lvzen4']
		lvzen5=self._zeninfo['lvzen5']
		lvzen6=self._zeninfo['lvzen6']
		zenmode=tb_zen_admin.getObj(self._owner.baseInfo.getId())
		zenmode.update_multi({'zenId':zenId,'lvzen1':lvzen1,'lvzen2':lvzen1,'lvzen2':lvzen3,'lvzen1':lvzen13,'lvzen4':lvzen4,'lvzen5':lvzen5,'lvzen6':lvzen6})
		return True