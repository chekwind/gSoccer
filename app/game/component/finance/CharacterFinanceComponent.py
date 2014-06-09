#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''
from app.game.component.Component import Component

class CharacterFinanceComponent(Component):
	'''
	finace component for character
	'''
	MAXCOIN=999999

	def __init__(self,owner,gamecoin=0,coin=0):
		'''
		Constructor
		'''
		Component.__init__(self,owner)
		self._gamecoin=gamecoin #角色的银币
		self._coin=coin #角色的金币

	#---------gamecoin---------
	def getGameCoin(self):
		return self._gamecoin

	def setGameCoin(self,gamecoin):
		self._gamecoin=gamecoin

	def updateGameCoin(self,gamecoin,state=1):
		if gamecoin==self._gamecoin:
			return
		if gamecoin>=self.MAXCOIN:
			self._gamecoin=self.MAXCOIN
		else:
			self._gamecoin=gamecoin

	def addGameCoin(self,gamecoin,state=1):
		gamecoin=self._gamecoin+gamecoin
		if gamecoin<0:
			return False
		self.updateGameCoin(gamecoin,state=state)
		return True

	#---------coin---------
	def getCoin(self):
		return self._coin

	def setCoin(self,coin,state=1):
		self._coin=coin

	def updateCoin(self,coin,state=1):
		delta=self._coin-coin
		if not delta:
			return
		self._coin=coin

	def consCoin(self,consCoin,consType,consDesc='',itemId=0):
		'''金币消耗
		@param consCoin : int  消耗的金币的数量
		@param consType : int  消耗的行为类型
		@param consDesc : int  消耗的描述
		@param itemId   : int  相关的物品的id
		'''
		self.addCoin(-consCoin)

	def addCoin(self,coin):
		nowcoin=self._coin+coin
		if nowcoin<0:
			return False
		self.updateCoin(nowcoin)
		return True