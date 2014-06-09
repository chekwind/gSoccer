#coding:utf8
'''
Created on 2014-2-27

@author: CC
'''
from app.game.component.Component import Component
import random
from app.share.dbopear import dbPlayer
from app.dbfront.memmode import tb_player_admin




class PlayerAttributeComponent(Component):
	'''球员属性相关'''

	def __init__(self,owner):
		'''
		Constructor
		@param Shoot:int 射门
		@param Dribbling: 带球
		@param Speed:速度
		@param Pass:传球
		@param Tackle:铲球
		@param Tackling:断球
		@param _Save:补救
		@param Response:出击
		'''
		Component.__init__(self,owner)
		self.Shoot=0
		self.Dribbling=0
		self.Speed=0
		self.Pass=0
		self.Tackle=0
		self.Tackling=0
		self._Save=0
		self.Response=0
		self.PlayerPower=0

	def initData(self,Shoot,Dribbling,Speed,Pass,Tackle,Tackling,_Save,Response):
		self.Shoot=Shoot
		self.Dribbling=Dribbling
		self.Speed=Speed
		self.Pass=Pass
		self.Tackle=Tackle
		self.Tackling=Tackling
		self._Save=_Save
		self.Response=Response

	def getAttribute(self):
		'''获取球员的属性'''
		info={}
		info['Shoot']=self.Shoot
		info['Dribbling']=self.Dribbling
		info['Speed']=self.Speed
		info['Pass']=self.Pass
		info['Tackle']=self.Tackle
		info['Tackling']=self.Tackling
		info['_Save']=self._Save
		info['Response']=self.Response
		info['PlayerPower']=int(self.CalculatePlayerPower()+0.5)
		return info

	def setAttribute(self,Shoot,Dribbling,Speed,Pass,Tackle,Tackling,_Save,Response):
		'''设置球员的属性'''
		self.Shoot=Shoot
		self.Dribbling=Dribbling
		self.Speed=Speed
		self.Pass=Pass
		self.Tackle=Tackle
		self.Tackling=Tackling
		self._Save=_Save
		self.Response=Response
		self.PlayerPower=int(self.CalculatePlayerPower()+0.5)

	def CalculatePlayerPower(self):
		'''计算球员的实力'''
		templateInfo=dbPlayer.PLAYER_TEMPLATE.get(self._owner.templateId)
		role=templateInfo['Role']
		playerpower=0
		if role==1:
			playerpower=(self.Shoot+self.Dribbling)*0.5*0.1+(self.Speed+self.Pass)*0.5*0.3+(self.Tackle+self.Tackling)*0.5*0.1+(self._Save+self.Response)*0.5*0.6
		elif role==2:
			playerpower=(self.Shoot+self.Dribbling)*0.5*0.2+(self.Speed+self.Pass)*0.5*0.3+(self.Tackle+self.Tackling)*0.5*0.5+(self._Save+self.Response)*0.5*0.1
		elif role==3:
			playerpower=(self.Shoot+self.Dribbling)*0.5*0.2+(self.Speed+self.Pass)*0.5*0.6+(self.Tackle+self.Tackling)*0.5*0.2+(self._Save+self.Response)*0.5*0.1
		elif role==4:
			playerpower=(self.Shoot+self.Dribbling)*0.5*0.5+(self.Speed+self.Pass)*0.5*0.3+(self.Tackle+self.Tackling)*0.5*0.2+(self._Save+self.Response)*0.5*0.1
		else:
			pass
		return playerpower

	def SaveAttribute(self):
		'''保存球员属性'''

		props={}
		props['Shoot']=self.Shoot
		props['Dribbling']=self.Dribbling
		props['Speed']=self.Speed
		props['Pass']=self.Pass
		props['Tackle']=self.Tackle
		props['Tackling']=self.Tackling
		props['_Save']=self._Save
		props['Response']=self.Response
		props['PlayerPower']=self.PlayerPower
		playermode=tb_player_admin.getObj(self._owner.baseInfo.getId())
		playermode.update_multi(props)
		return {'result':True,'message':u""}

