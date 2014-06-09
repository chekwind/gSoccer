#coding:utf8
'''
Created on 2014-2-25

@author: CC
'''
from app.game.core.character.Character import Character
from app.game.component.player.NPCPlayerComponent import NPCPlayerComponent
from app.game.component.attribute.CharacterAttributeComponent import CharacterAttributeComponent
from app.share.dbopear import dbclub

class NPCClub(Character):
	'''NPC球队类'''


	def __init__(self,id=-1,name='',templateId=0,zenId=1,clubcategory=1):
		'''初始化NPC球队类'''
		data={}
		if clubcategory==1:#挑战赛球队
			data=dbclub.CHALLENGENPC.get(templateId)
		elif clubcategory==7:#训练赛球队
			data=dbclub.TRAINMATCHNPC.get(templateId)
		Character.__init__(self,id,name)
		self.setCharacterType(Character.CLUBTYPE)
		self.player=NPCPlayerComponent(self)#npc球队球员
		self.attribute=CharacterAttributeComponent(self) #npc球队属性
		self.templateId=int(data['ID'])
		self.formatInfo={}
		self.initialiseToo(data)


	def initialiseToo(self,data):
		'''初始化NPC球队信息
		@param id:int npc球队ID
		'''
		self.formatInfo['templateId']=data['ID']
		self.formatInfo['clubname']=data['ClubName']
		self.formatInfo['leagueindex']=data['LeagueIndex']
		self.formatInfo['leaguename']=data['LeagueName']
		self.formatInfo['zenid']=data['ZenID']
		self.formatInfo['clublogo']=data['ClubLogo']
		self.formatInfo['powerindex']=data['PowerIndex']
		self.formatInfo['clubpower']=data['ClubPower']
		self.formatInfo['clubcategory']=data['ClubCategory']
		self.player.initPlayerInfo(data['ID'])

	def getNPCType(self):
		'''获取NPC球队类型'''
		return self.formatInfo.get('clubcategory')

	def getZenId(self):
		'''获取NPC球队的战术ID'''
		return self.formatInfo.get('zenid')

	def getClubPower(self):
		'''获取NPC球队的实力'''
		return self.formatInfo.get('clubpower')

	def getNPCInfo(self):
		'''获取npc球队信息'''
		return self.formatInfo

	def getNPCPlayers(self):
		'''获取npc球员信息'''
		return self.player.getPlayerListInfo()


