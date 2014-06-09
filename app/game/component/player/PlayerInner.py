#coding:utf8
'''
Created on 2014-2-13

@author: CC
'''
from app.game.component.Component import Component
import random,time,datetime
from app.game.appinterface import configure
from app.share.dbopear import dbPlayer,dbPlayerInner

def getplayersuiji_bai():
	'''百里挑一随机'''
	while True:
		rate=random.randint(1,100000)
		if rate>99000:
			yield 4 #杰出
		elif rate>85000:
			yield 3 #精英
		elif rate>50000:
			yield 2 #优秀
		else:
			yield 1 #普通

def getplayersuiji_qian():
	'''千里挑一随机'''
	while True:
		rate=random.randint(1,100000)
		if rate>99900:
			yield 6 #巨星
		elif rate>85000:
			yield 5 #大牌
		elif rate>50000:
			yield 4 #杰出
		else:
			yield 3 #精英

def getplayersuiji_wan():
	'''万里挑一随机'''
	while True:
		rate=random.randint(1,100000)
		if rate>95000:
			yield 6 #巨星
		elif rate>70000:
			yield 5 #大牌
		else:
			yield 4 #杰出

PQ_Generater_bai=getplayersuiji_bai()
PQ_Generater_qian=getplayersuiji_qian()
PQ_Generater_wan=getplayersuiji_wan()
DISSMISSPOINT={
	1:1,
	2:2,
	3:5,
	4:8,
	5:12,
	6:20
}#各品质球员遣散返还的搜寻点


class PlayerInner(Component):
	'''寻找球员'''

	def __init__(self,owner):
		'''初始化寻找球员'''
		Component.__init__(self,owner)
		self.owner=owner
		self.ctime1="None"#百里挑一记录时间
		self.ctime2="None"#千里挑一记录时间
		self.inner=[0,0,0]#找到的球员
		self.cs1=10#百里挑一免费次数
		self.cs2=3#千里挑一免费次数
		self.xy=0#幸运值
		self.point=0#搜寻点
		self.indb=0#是否已经写入数据库
		self.initPlayerInner()

	def initPlayerInner(self):
		'''初始化寻找球员信息'''
		characterId=self._owner.baseInfo.id
		info=dbPlayerInner.getByid(characterId)#剩余时间记录
		if info:
			self.ctime1=info.get('ctime1')
			self.ctime2=info.get('ctime2')
			self.xy=info.get('xy')
			self.point=info.get('point')
			self.refleshInner()		
			self.cs1=info.get('cs1')#百里挑一免费次数
			self.cs2=info.get('cs2')#千里挑一免费次数
			self.indb=1
		else:
			self.inner[0]=10807
			self.UpdateInner(2)
			self.UpdateInner(3)

	def refleshInner(self,purview=0):
		'''获取寻找到的球员'''
		self.FillInner()
		if purview==1:
			self.ctime1=time.time()
			self.ctime2=time.time()


	def FillInner(self):
		'''填充找到的球员'''
		playerlist=[]
		for i in range(1,4):
			playerlist.append(self.findOnePlayer(i))
		self.inner=playerlist

	def UpdateInner(self,i,leagueindex=1):
		'''更新找到的球员
		@param i:int 类型: 1百 2千 3万
		@param leagueindex:int 联赛类型: 1法 2德 3意 4英 5西
		'''
		self.inner[i-1]=self.findOnePlayer(i,leagueindex)

		
	def findOnePlayer(self,i,leagueindex=1):
		'''寻找一个球员
		@param i:int 类型: 1百 2千 3万
		@param leagueindex:int 联赛类型: 1法 2德 3意 4英 5西
		'''
		if i==1:
			quality=PQ_Generater_bai.next()
		elif i==2:
			quality=PQ_Generater_qian.next()
		elif i==3:	
			quality=PQ_Generater_wan.next()
		inner=self.getInnerByLQ(quality,leagueindex)#球员模板信息列表
		count=len(inner)
		index=random.randint(0,count-1)
		return inner[index]

	def getTime(self,Type):
		'''获取剩余冷却时间'''
		if Type==1 and self.ctime1!="None":#百里挑一
			s=configure.getchaTime(self.ctime1,configure.m(10))
			return s
		elif Type==2 and self.ctime2!="None":#千里挑一
			s=configure.getchaTime(self.ctime2,configure.h(24))
			return s
		else:
			return 0

	def getsycs(self,Type):
		'''获取每天剩余免费次数'''
		if Type==1:
			if self.cs1<0:
				self.cs1=0
			return self.cs1
		elif Type==2:
			if self.cs2<0:
				self.cs2=0
			return self.cs2


	def addXy(self,count):
		'''增加幸运值
		@param count:int 增加的数量
		'''
		self.xy+=count

	def updatePoint(self,point):
		'''更新搜寻点
		@param count:int 更新的数量
		'''
		self.point+=point


	def getInnerByLQ(self,quality,leagueindex=1):
		'''根据联赛和球员品质获取可寻找球员
		@param leagueindex:int 联赛类型: 1法 2德 3意 4英 5西
		@param quality:int 球员品质
		'''
		playerlist=[]
		players=dbPlayer.PLAYER_TEMPLATE_FINDABLE[leagueindex]
		for player in players.values():
			if player['PlayerQuality']==quality:
				playerlist.append(player['id'])
		return playerlist

	def pickPlayer(self,picktype,costpoint,leagueindex):
		'''挑选球员
		@param picktype:int 挑选类型
		@param costpoint:int 消耗点数
		@param leagueindex:int 联赛类型
		'''
		info={}
		if picktype==1:#百里挑一
			if self.cs1>0 and self.getTime(picktype)<=0:#已冷却且免费次数>0
				self.cs1-=1	
				self.ctime1=datetime.datetime.now()
				self.UpdateInner(picktype,leagueindex)
			elif self.point>costpoint:#点数足够
				self.point-=costpoint
				self.ctime1=datetime.datetime.now()
				self.UpdateInner(picktype,leagueindex)
			else:
				return {'result':False,'message':u"点数不够"}
			info={'playerid':self.inner[0],'point':self.point,'ctime':self.getTime(picktype),'cs':self.cs1}
			return {'result':True,'data':info}
		elif picktype==2:#千里挑一
			if self.cs2>0 and self.getTime(picktype)<=0:#已冷却且免费次数>0
				self.cs2-=1			
				self.ctime2=datetime.datetime.now()
				self.UpdateInner(picktype,leagueindex)
			elif self.point>costpoint:#点数足够
				self.point-=costpoint
				self.ctime1=datetime.datetime.now()
				self.UpdateInner(picktype,leagueindex)		
			else:
				return {'result':False,'message':u"点数不够"}
			info={'playerid':self.inner[1],'point':self.point,'ctime':self.getTime(picktype),'cs':self.cs2}
			return {'result':True,'data':info}
		elif picktype==3:#万里挑一
			if self.point>costpoint:#点数足够
				self.UpdateInner(picktype,leagueindex)
				self.point-=costpoint
				info={'playerid':self.inner[2],'point':self.point,'ctime':0,'cs':0}
				return {'result':True,'data':info}
			else:
				return {'result':False,'message':u"点数不够"}
		else:
			return {'result':False,'message':u"抽取球员失败"}

	def dbupdate(self):
		'''下线处理中，将信息记录到数据库中'''
		characterId=self._owner.baseInfo.id
		ctime1=self.ctime1
		ctime2=self.ctime2
		cs1=self.cs1
		cs2=self.cs2
		xy=self.xy
		point=self.point
		if self.indb:
			dbPlayerInner.updateInfo(characterId,ctime1,ctime2,cs1,cs2,xy,point)
		else:
			dbPlayerInner.addInfo(characterId,ctime1,ctime2,cs1,cs2,xy,point)

