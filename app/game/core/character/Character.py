#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.game.component.baseInfo.CharacterBaseInfoComponent import CharacterBaseInfoComponent

class Character(object):
	'''角色通用类'''

	GAMERTYPE=1 #玩家
	CLUBTYPE=2#NPC
	PLAYERTYPE=3 #球员
	MAXPOWER=100 #能量最大值

	def __init__(self,cid,name):
		'''
			创建一个角色
		'''
		self.baseInfo=CharacterBaseInfoComponent(self,cid,name)
		self.CharacterType=0 # 角色的类型

	def setCharacterType(self,characterType):
		'''设置角色类型'''
		self.CharacterType=characterType

	def getCharacter(self):
		'''获取角色类型
		'''
		return self.CharacterType

	def getBaseID(self):
		return self.baseInfo.id