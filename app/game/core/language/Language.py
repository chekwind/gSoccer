#coding:utf8
'''
Created on 2014-3-20

@author: CC
'''
from gfirefly.utils.singleton import Singleton
from gtwisted.utils import log
from app.share.dbopear import dbLanguage

class Lg:
	'''语言包'''
	__metaclass__=Singleton

	def __init__(self):
		'''初始化'''
		self.info={}
		self.info=dbLanguage.getAll()

	def Update(self):
		'''更新数据信息'''
		self.info=dbLanguage.getAll()

	def g(self,gid):
		'''根据id获取翻译信息'''
		try:
			info=self.info.get(gid)
			if not info:
				log.err(str(gid))
				return str(gid)
			return info
		except:
			return str(gid)
			log.err("%s不存在"%gid)
