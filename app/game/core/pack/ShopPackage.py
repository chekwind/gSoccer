#coding:utf8
'''
Created on 2014-2-24

@author: CC
'''

from app.game.component.pack.BasePackage import BasePackage

class ShopPackage():
	'''商店包裹'''
	def __init__(self):
		'''商店包裹'''
		self.gamecoinShopPackage=BasePackage(48)
		self.coinShopPackage=BasePackage(48)

	def putItemShopPackage(self,shopType,item):
		'''放置一个物品到商店包裹中
		@param shopType:int 商店类型
		'''
		if shopType==1:
			pass
		elif shopType==2:
			pass