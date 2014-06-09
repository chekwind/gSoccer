#coding:utf8
'''
Created on 2014-2-25

@author: CC
'''
from gfirefly.utils.singleton import Singleton

class ShopManager:
	'''商店管理器'''

	__metaclass__=Singleton

	def __init__(self):
		'''初始化商店管理器'''
		self._shops={}

	def addShop(self,shop):
		'''添加一个商店
		@param shop: Shop Object
		'''
		self._shops[shop._shopcategory]=shop

	def dropShopByCategory(self,shopCategory):
		'''删除商店
		@param shopCategory: int 商店的类型
		'''
		try:
			del self._shops[shopCategory]
		except Exception:
			pass

	def getShopByCategory(self,shopCategory):
		'''根据商店类型获取商店'''
		return self._shops.get(shopCategory,None)
