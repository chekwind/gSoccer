#coding:utf8
'''
Created on 2014-2-25

@author: CC
'''
from .Character import Character
from app.game.component.level.PlayerLevelComponent import PlayerLevelComponent
from app.game.component.attribute.PlayerAttributeComponent import PlayerAttributeComponent
from twisted.python import log

from app.share.dbopear import dbPlayer,dbCharacter
from app.dbfront.memmode import tb_player_admin
import datetime

MAX_ATTRIBUTE_BILI={1:22,2:30,3:40,4:52,5:66,6:82,7:100,8:120,9:140}

class Player(Character):
	'''球员类'''

	def __init__(self,playerId=0,name='',templateId=0,owner=0,level=1,PlayerCategory=2,PlayerPos='z'):
		'''初始化球员信息'''
		Character.__init__(self,playerId,name)
		self.setCharacterType(self.PLAYERTYPE)
		self.templateId=templateId
		self._owner=owner#球员所在球队的ID
		self.level=PlayerLevelComponent(self,level=level,exp=0)
		self.attribute=PlayerAttributeComponent(self)
		self.PlayerPos=PlayerPos
		self.PlayerCategory=PlayerCategory
		self.SpendPoint=0
		if self.templateId:
			self.initData()

	def initData(self):
		'''不存在实例时的初始化方式'''
		templateinfo=dbPlayer.PLAYER_TEMPLATE.get(self.templateId)
		if not templateinfo:
			log.err("Player template %d not exits"%self.templateId)
		self.baseInfo.setName(templateinfo.get('PlayerName',''))
		self.level.setPlayerQuality(templateinfo.get('PlayerQuality'))
		Shoot=templateinfo.get('Shoot')
		Dribbling=templateinfo.get('Dribbling')
		Speed=templateinfo.get('Speed')
		Pass=templateinfo.get('Pass')
		Tackle=templateinfo.get('Tackle')
		Tackling=templateinfo.get('Tackling')
		Save=templateinfo.get('_Save')
		Response=templateinfo.get('Response')
		self.attribute.initData(Shoot,Dribbling,Speed,Pass,Tackle,Tackling,Save,Response)

	def initPlayerInstance(self,playerInstanceData):
		'''存在数据库实例时的初始化方式'''
		self.templateId=playerInstanceData.get('PlayertemplateID')
		Shoot=playerInstanceData.get('Shoot')
		Dribbling=playerInstanceData.get('Dribbling')
		Speed=playerInstanceData.get('Speed')
		Pass=playerInstanceData.get('Pass')
		Tackle=playerInstanceData.get('Tackle')
		Tackling=playerInstanceData.get('Tackling')
		Save=playerInstanceData.get('_Save')
		Response=playerInstanceData.get('Response')
		self._owner=playerInstanceData.get('cid')
		self.attribute.initData(Shoot,Dribbling,Speed,Pass,Tackle,Tackling,Save,Response)
		self.level.setExp(playerInstanceData.get('Exp'))
		self.level.setLevel(playerInstanceData.get('Level'))
		self.setSpendPoint(playerInstanceData.get('SpendPoint'))
		self.setPlayerpos(playerInstanceData.get('PlayerPos'))
		self.setPlayerCategory(playerInstanceData.get('PlayerCategory'))
		templateinfo=dbPlayer.PLAYER_TEMPLATE.get(self.templateId)
		self.level.setPlayerQuality(templateinfo.get('PlayerQuality'))
		if playerInstanceData.get('PlayerName'):
			self.baseInfo.setName(playerInstanceData.get('PlayerName',''))
		else:
			self.baseInfo.setName(templateinfo.get('PlayerName',''))

	@property
	def templateInfo(self):
		return dbPlayer.PLAYER_TEMPLATE.get(self.templateId)

	def InsertIntoDB(self):
		'''将不存在的实例写入数据库，生成数据库中的实例'''
		cid=self._owner
		templateinfo=dbPlayer.PLAYER_TEMPLATE.get(self.templateId)
		Shoot=templateinfo.get('Shoot')
		Dribbling=templateinfo.get('Dribbling')
		Speed=templateinfo.get('Speed')
		Pass=templateinfo.get('Pass')
		Tackle=templateinfo.get('Tackle')
		Tackling=templateinfo.get('Tackling')
		Save=templateinfo.get('_Save')
		Response=templateinfo.get('Response')
		PlayerPower=templateinfo.get('PlayerPower')
		level=self.level.getLevel()
		data={'cid':cid,
			  'PlayertemplateID':self.templateId,
			  'Accesstime':str(datetime.datetime.today()),
			  'PlayerName':templateinfo.get('PlayerName'),
			  'Level':level,
			  'Exp':0,
			  'PlayerPos':self.PlayerPos,
			  'PlayerCategory':self.PlayerCategory,
			  'Shoot':Shoot,
			  'Dribbling':Dribbling,
			  'Speed':Speed,
			  'Pass':Pass,
			  'Tackle':Tackle,
			  'Tackling':Tackling,
			  '_Save':Save,
			  'Response':Response,
			  'PlayerPower':PlayerPower,
			  'SpendPoint':0,}
		playermmode=tb_player_admin.new(data)
		playerId=int(playermmode._name.split(':')[1])
		if playerId:
			self.baseInfo.setId(playerId)
			return True
		return False

	def destoryByDB(self):
		'''删除球员在数据库中的数据'''
		tb_player_admin.deleteMode(self.baseInfo.id)
		return True

	def SavePlayerAttribute(self):
		'''保存球员属性'''
		result=self.attribute.SaveAttribute()
		return result

	def PlayerTraining(self,Shoot,Dribbling,Speed,Pass,Tackle,Tackling,_Save,Response,Trainpoint,gamer):
		'''训练球员'''
		templateinfo=dbPlayer.PLAYER_TEMPLATE.get(self.templateId)
		attrinfo=self.attribute.getAttribute()
		level=self.level.getLevel()
		bili=MAX_ATTRIBUTE_BILI.get(level)
		maxtrainpoint=0
		if Shoot<=self.max_attr(templateinfo['Shoot'],bili):
			if Shoot>=attrinfo['Shoot']:maxtrainpoint+=self.TrainPointState(Shoot,attrinfo['Shoot'])
			else:return False
		else:return False

		if Dribbling<=self.max_attr(templateinfo['Dribbling'],bili):
			if Dribbling>=attrinfo['Dribbling']:maxtrainpoint+=self.TrainPointState(Dribbling,attrinfo['Dribbling'])
			else:return False
		else:return False

		if Speed<=self.max_attr(templateinfo['Speed'],bili):
			if Speed>=attrinfo['Speed']:maxtrainpoint+=self.TrainPointState(Speed,attrinfo['Speed'])
			else:return False
		else:return False

		if Pass<=self.max_attr(templateinfo['Pass'],bili):
			if Pass>=attrinfo['Pass']:maxtrainpoint+=self.TrainPointState(Pass,attrinfo['Pass'])
			else:return False
		else:return False

		if Tackle<=self.max_attr(templateinfo['Tackle'],bili):
			if Tackle>=attrinfo['Tackle']:maxtrainpoint+=self.TrainPointState(Tackle,attrinfo['Tackle'])
			else:return False
		else:return False

		if Tackling<=self.max_attr(templateinfo['Tackling'],bili):
			if Tackling>=attrinfo['Tackling']:maxtrainpoint+=self.TrainPointState(Tackling,attrinfo['Tackling'])
			else:return False
		else:return False

		if _Save<=self.max_attr(templateinfo['_Save'],bili):
			if _Save>=attrinfo['_Save']:maxtrainpoint+=self.TrainPointState(_Save,attrinfo['_Save'])
			else:return False
		else:return False

		if Response<=self.max_attr(templateinfo['Response'],bili):
			if Response>=attrinfo['Response']:maxtrainpoint+=self.TrainPointState(Response,attrinfo['Response'])
			else:return False
		else:return False
		ctrainpoint=gamer.attribute.getTrainPoint()
		if ctrainpoint>=maxtrainpoint:
			gamer.attribute.setTrainPoint(ctrainpoint-maxtrainpoint)
			self.updateSpendPoint(self.SpendPoint+maxtrainpoint)
			self.attribute.setAttribute(Shoot,Dribbling,Speed,Pass,Tackle,Tackling,_Save,Response)
			return True
		return False

	def getPlayerpos(self):
		'''获取球员场上位置'''
		return self.PlayerPos

	def setPlayerpos(self,playerpos):
		'''设置球员场上位置'''
		self.PlayerPos=playerpos

	def getPlayerCategory(self):
		'''获取球员种类'''
		return self.PlayerCategory

	def setPlayerCategory(self,playercategory):
		'''设置球员种类'''
		self.PlayerCategory=playercategory

	def getSpendPoint(self):
		'''获取消耗的训练点'''
		return self.SpendPoint

	def setSpendPoint(self,spendpoint):
		'''设置消耗的训练点'''
		self.SpendPoint=spendpoint

	def updateSpendPoint(self,spendpoint):
		'''更新球员消耗训练点
		@param spendpoint: int 消耗的训练点
		'''
		self.setSpendPoint(spendpoint)
		playermode=tb_player_admin.getObj(self.baseInfo.id)
		props={'SpendPoint':spendpoint}
		playermode.update_multi(props)


	def formatPlayerInfo(self):
		'''格式化球员信息'''
		templateinfo=dbPlayer.PLAYER_TEMPLATE.get(self.templateId)
		attrinfo=self.attribute.getAttribute()
		bili=MAX_ATTRIBUTE_BILI.get(self.level.getLevel())
		info=attrinfo
		info['id']=self.baseInfo.getId()#球员的实例ID
		info['PlayerName']=self.baseInfo.getName()#球员的名字
		info['Role']=templateinfo.get('Role')
		info['PlayerPos']=self.PlayerPos
		info['PlayerCategory']=self.PlayerCategory
		info['PlayerQuality']=templateinfo.get('PlayerQuality')
		info['Photo']=templateinfo.get('Photo','')
		info['Nationality']=templateinfo.get('Nationality')
		info['Height']=templateinfo.get('Height')
		info['Weight']=templateinfo.get('Weight')
		info['SpendPoint']=self.SpendPoint
		info['Level']=self.level.getLevel()
		info['Exp']=self.level.getExp()
		info['MaxExp']=self.level.getMaxExp()
		info['MaxShoot']=self.max_attr(templateinfo['Shoot'],bili)
		info['MaxDribbling']=self.max_attr(templateinfo['Dribbling'],bili)
		info['MaxSpeed']=self.max_attr(templateinfo['Speed'],bili)
		info['MaxPass']=self.max_attr(templateinfo['Pass'],bili)
		info['MaxTackling']=self.max_attr(templateinfo['Tackling'],bili)
		info['MaxTackle']=self.max_attr(templateinfo['Tackle'],bili)
		info['MaxSave']=self.max_attr(templateinfo['_Save'],bili)
		info['MaxResponse']=self.max_attr(templateinfo['Response'],bili)
		return info

	def max_attr(self,attribute,bili):
		'''计算能力最高值'''
		return (attribute-35)*bili/7

	def TrainPointState(self,BigPoint,LittlePoint):
		'''计算消耗点数'''
		MadeTrianPoint=0
		for i in range(0,BigPoint-LittlePoint):
			MadeTrianPoint += (LittlePoint + i + 50) / 5
		return MadeTrianPoint

	def addPlayerExp(self,exp):
		'''球员加经验'''
		result=self.level.addExp(exp)
		return result
	def upgradePlayer(self):
		'''球员升级'''
		result=self.level.updateLevel()
		return result

	def savePlayerpos(self,playerpos,playercategory):
		'''保存球员位置与类型'''
		self.setPlayerpos(playerpos)
		self.setPlayerCategory(playercategory)
		playermode=tb_player_admin.getObj(self.baseInfo.id)
		props={'PlayerPos':playerpos,'PlayerCategory':playercategory}
		playermode.update_multi(props)





