#coding:utf8
'''
Created on 2014-3-6

@author: CC
'''
import random

bases={}
class TrainBase:
	'''训练基地类'''

	def __init__(self):
		pass

	def initTrainBase(self):
		'''初始化训练基地'''
		for i in range(1,11):
			base={}
			base['trainpoint']=int(3000*(1+random.randrange(0,100,2)*0.01))
			base['status']=0
			base['occupier']=0
			bases[i]=base

	def getTrainBase(self):
		'''获取训练基地信息'''
		return bases

	def setTainBaseStatus(self,num,status,occupier=0):
		'''更新训练基地状态'''
		base=bases.get(num)
		base['status']=status
		base['occupier']=occupier
