#coding:utf8
'''
Created on 2014-2-26

@author: CC
'''
from app.game.component.Component import Component
from app.share.dbopear import dbPlayer
from app.dbfront.memmode import tb_player_admin

class PlayerLevelComponent(Component):
	'''球员等级组件类'''
	def __init__(self,owner,level=1,exp=0,playerquality=1):
		'''
		@param owner: Character Object 组件拥有者
		@param level: int 球员的等级
		@param exp: 球员的当前经验
		'''
		Component.__init__(self,owner)
		self._level=level
		self._exp=exp
		self._playerquality=playerquality

	def getLvExp(self):
		'''计算当前级别升级所需经验值'''
		quality_exp=dbPlayer.PLAYER_EXP.get(self._playerquality)
		lvExp=quality_exp.get(self._level,0)
		return int(lvExp)

	def getMaxExp(self):
		'''获取球员最高经验值'''
		quality_exp=dbPlayer.PLAYER_EXP.get(self._playerquality)
		maxExp=quality_exp.get(self.getLevel(),0)
		return int(maxExp)

	def getExp(self):
		'''获取球员当前经验'''
		return self._exp

	def setExp(self,exp):
		'''设置球员当前经验值
		@param exp:int 经验值
		'''
		self._exp=exp

	def updateExp(self,exp):
		'''更新球员经验值
		@param exp:int 经验值
		'''
		if exp==self._exp or exp>=self.getMaxExp():
			return False
		if self._level>=self.getMaxLevel():
			return False
		self._exp=exp
		playermode=tb_player_admin.getObj(self._owner.baseInfo.getId())
		playermode.update_multi({'exp':self._exp})
		return True

	def addExp(self,exp):
		'''加经验'''
		result=self.updateExp(exp+self.getExp())
		return result

	def getLevel(self):
		'''获取球员当前等级'''
		return self._level

	def setLevel(self,level):
		'''设置球员当前等级
		@param level:int 等级
		'''
		self._level=level

	def updateLevel(self):
		'''更新球员当前等级
		'''
		if self._level>self.getMaxLevel():return False
		while self._exp >= self.getLvExp():
			#self._exp -= self.getLvExp()
			self._level += 1
		playermode=tb_player_admin.getObj(self._owner.baseInfo.getId())
		playermode.update_multi({'level':self._level})
		return True

	def getAllExp(self):
		'''获取所有的可传承经验'''
		allExp=100
		level=self.getLevel()
		quality_exp=dbPlayer.PLAYER_EXP.get(self._playerquality)
		while level>1:
			level-=1
			allExp+=quality_exp.get(level)
		allExp+=self.getExp()
		return allExp/2

	def ForecastLevelUp(self,exp):
		'''预测可能提升的等级'''
		nowallexp=self._exp+exp
		lastlevel=self._level
		quality_exp=dbPlayer.PLAYER_EXP.get(self._playerquality)
		if self._level>=self.getMaxLevel():
			return self.getMaxLevel()
		while nowallexp>=self.getMaxExp():
			nowallexp-=quality_exp.get(lastlevel)
			lastlevel+=1
		return lastlevel

	def getMaxLevel(self):
		'''获取球员最高等级'''
		playerid=self._owner.baseInfo.getId()
		return self._playerquality+2

	def getPlayerQuality(self):
		'''获取球员品质'''
		return self._playerquality

	def setPlayerQuality(self,playerquality):
		'''设置球员品质'''
		self._playerquality=playerquality