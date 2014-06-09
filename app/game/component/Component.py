#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

class Component(object):
	'''
	抽象的组件对象
	'''

	def __init__(self,owner):
		'''
		创建一个组件
		@param owner:owner of this component
		'''
		self._owner=owner