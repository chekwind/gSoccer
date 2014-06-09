#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.game.component.Component import Component
from app.game.component.zen.CharacterZenComponent import CharacterZenComponent
from app.share.dbopear import dbZen
import time

ENERGY_TIME=1800#隔30分钟涨一点活力

PLAYERCHANGEPOS_POWER={
	1:{'oldrole':1,'newrole':1,'Percentage':100},
	2:{'oldrole':1,'newrole':2,'Percentage':10},
	3:{'oldrole':1,'newrole':3,'Percentage':10},
	4:{'oldrole':1,'newrole':4,'Percentage':10},
	5:{'oldrole':2,'newrole':1,'Percentage':10},
	6:{'oldrole':2,'newrole':2,'Percentage':100},
	7:{'oldrole':2,'newrole':3,'Percentage':70},
	8:{'oldrole':2,'newrole':4,'Percentage':30},
	9:{'oldrole':3,'newrole':1,'Percentage':10},
	10:{'oldrole':3,'newrole':2,'Percentage':50},
	11:{'oldrole':3,'newrole':3,'Percentage':100},
	12:{'oldrole':3,'newrole':4,'Percentage':50},
	13:{'oldrole':4,'newrole':1,'Percentage':10},
	14:{'oldrole':4,'newrole':2,'Percentage':30},
	15:{'oldrole':4,'newrole':3,'Percentage':70},
	16:{'oldrole':4,'newrole':4,'Percentage':100}
}
JIACHENG={
	'Low':{0:1,1:2,2:3,3:5,4:6,5:8,6:9,7:11,8:12,9:14,10:15},
	'Advanced':{0:8,1:20,2:22,3:24,5:28,6:30,7:32,8:34,9:37,10:40}
}


class CharacterAttributeComponent(Component):

	MAXENERGY=200
	'''角色属性组件类'''
	def __init__(self,owner,energy=200,trainpoint=1000):
		'''Constructor'''
		Component.__init__(self,owner)

		self._energy=energy#当前活力
		self._timestamp=time.time()
		self._photo='null.png'
		self._power=0
		self._maxpower=0
		self._trainpoint=trainpoint
		self._tacticspoint=0
		self._repute=0
		self.jingong=0
		self.zuzhi=0
		self.fangshou=0
		self.shoumen=0

	def getExpEff(self):
		'''获取经验获取百分百'''
		effectExpEff=1
		return effectExpEff

	def getEnergy(self):
		'''获取角色当前活力值'''
		energyadd=self.calculateEnergy()
		self._energy=self._energy+energyadd
		return self._energy

	def calculateEnergy(self):
		'''计算活力增长值'''
		nowtime=time.time()
		delta=int(nowtime-self._timestamp)
		energy=delta/ENERGY_TIME
		self._timestamp+=energy*ENERGY_TIME
		return energy

	def initEnergy(self,energy):
		'''初始化活力'''
		outtime=0
		now=int(time.time())
		t1=int(now)/ENERGY_TIME
		t2=int(outtime)/ENERGY_TIME
		energyadd=int(t1-t2)
		sptime=int(now)%ENERGY_TIME
		self._timestamp=now-sptime
		nowenergy=energy+energyadd
		self.setEnergy(nowenergy)

	def setEnergy(self,energy):
		'''设置角色活力'''
		if energy>self.MAXENERGY:
			self._energy=self.MAXENERGY
		else:
			self._energy=energy

	def updateEnergy(self,energy):
		'''更新角色活力'''
		maxEnergy=self.MAXENERGY
		if energy>maxEnergy:
			energy=maxEnergy
		elif energy<0:
			energy=0
		self._energy=energy

	def addEnergy(self,energy):
		'''加活力'''
		nowenergy=self._energy+energy
		self.setEnergy(nowenergy)

	def getPhoto(self):
		'''获取角色头像'''
		return self._photo

	def setPhoto(self,photo):
		'''设置角色头像'''
		self._photo=photo

	def getPower(self):
		'''获取当前实力'''
		return self._power

	def setPower(self,power):
		'''设置当前实力'''
		self._power=power

	def getMaxPower(self):
		'''获取最高实力'''
		return self._maxpower

	def setMaxPower(self,maxpower):
		'''设置最高实力'''
		self._maxpower=maxpower

	def getTrainPoint(self):
		'''获取训练点'''
		return self._trainpoint

	def setTrainPoint(self,trainpoint):
		'''设置训练点'''
		self._trainpoint=trainpoint

	def addTrainPoint(self,trainpoint):
		'''加训练点'''
		nowtrainpoint=self._trainpoint+trainpoint
		self.setTrainPoint(nowtrainpoint)

	def getTacticsPoint(self):
		'''获取战术点'''
		return self._tacticspoint

	def setTacticsPoint(self,tacticspoint):
		'''设置战术点'''
		self._tacticspoint=tacticspoint

	def addTacticsPoint(self,tacticspoint):
		'''加战术点'''
		nowtacticspoint=self._tacticspoint+tacticspoint
		self.setTacticsPoint(nowtacticspoint)	

	def getRepute(self):
		'''获取声望值'''
		return self._repute

	def setRepute(self,repute):
		'''设置声望值'''
		self._repute=repute

	def addRepute(self,repute):
		'''加声望值'''
		nowrepute=self._repute+repute
		self.setRepute(nowrepute)

	def calClubPower(self,zenid=1,zenlv=0):
		'''计算球队实力
		@param zenid:int 当前战术
		@param zenlv:int 当前战术等级
		'''
		jiacheng=0#战术加成
		zonghe=0#综合能力
		jingong=0#进攻
		zuzhi=0#组织
		fangshou=0#防守
		shoumen=0#守门
		players=[]
		if zenid in(1,3,5):
			jiacheng=JIACHENG['Low'][zenlv]#低级战术加成
		else:
			jiacheng=JIACHENG['Advanced'][zenlv]#高级战术加成

		for player in self._owner.player.getPlayers().values():
			if player.getPlayerpos()>='a' and player.getPlayerpos()<'z':#场上球员
				info=player.formatPlayerInfo()
				players.append(info)
		if len(players)!=11:#球员不是11人
			return self._power

		for player in players:
			oldrole=player['Role']
			playerpos=player['PlayerPos']
			role=dbZen.getZenconfigRole(zenid,playerpos)
			percent=0.0#百分比
			for i in PLAYERCHANGEPOS_POWER.values():
				if i['oldrole']==oldrole and i['newrole']==role:
					percent=i['Percentage']/100.0
					break
			zonghe+=player['PlayerPower']*percent
			if role==4:
				jingong+=(player['Shoot']**0.6666666667*(jiacheng+100)/100+player['Dribbling']**0.6666666667*(jiacheng+100)/100)*0.5*percent
			elif role==3:
				jingong+=(player['Shoot']**0.6666666667*(jiacheng+100)/100+player['Dribbling']**0.6666666667*(jiacheng+100)/100)*0.5*percent
				zuzhi+=(player['Speed']**0.6666666667*(jiacheng+100)/100+player['Pass']**0.6666666667*(jiacheng+100)/100)*0.5*percent
				fangshou+=(player['Tackle']**0.6666666667*(jiacheng+100)/100+player['Tackling']**0.6666666667*(jiacheng+100)/100)*0.5*percent
			elif role==4:
				fangshou+=(player['Tackle']**0.6666666667*(jiacheng+100)/100+player['Tackling']**0.6666666667*(jiacheng+100)/100)*0.5*percent
			elif role==1:
				shoumen+=(player['_Save']**0.6666666667*(jiacheng+100)/100+player['Response']**0.6666666667*(jiacheng+100)/100)*0.5*percent
				
		zonghe=zonghe*(jiacheng+100)/100
		self._power=int(zonghe+0.5)

		self.jingong,self.zuzhi,self.fangshou,self.shoumen=jingong,zuzhi,fangshou,shoumen

		if zenid in (1,2):
			self._power=int(zonghe+jingong*0.5+0.5)
		elif zenid in (3,4):
			self._power=int(zonghe+zuzhi*0.67+0.5)
		elif zenid in(5,6):
			self._power=int(zonghe+fangshou*0.33+shoumen*0.33+0.5)

		if self._power>self.getMaxPower():
			self.setMaxPower(self._power)

		return self._power

	def getMatchData(self):
		'''获取比赛相关信息'''
		return self.jingong,self.zuzhi,self.fangshou,self.shoumen,self._power




			



