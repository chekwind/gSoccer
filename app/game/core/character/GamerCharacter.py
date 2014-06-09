#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.game.core.character.Character import Character
from app.game.component.level.CharacterLevelComponent import CharacterLevelComponent
from app.game.component.finance.CharacterFinanceComponent import CharacterFinanceComponent
from app.game.component.attribute.CharacterAttributeComponent import CharacterAttributeComponent
from app.game.component.pack.CharacterPackComponent import CharacterPackageComponent
from app.game.component.mail.CharacterMailListComponent import CharacterMailListComponent
from app.game.component.shop.CharacterShopComponent import CharacterShopComponent
from app.game.component.zen.CharacterZenComponent import CharacterZenComponent
from app.game.component.task.CharacterTaskComponent import CharacterTaskComponent
from app.game.component.match.TrainMatchComponent import TrainMatchComponent
from app.game.component.match.ChallengeMatchComponent import ChallengeMatchComponent
from app.game.component.player.PlayerComponent import PlayerComponent
from app.game.component.player.PlayerInner import PlayerInner
from app.dbfront.memmode import tb_character_admin

class GamerCharacter(Character):
	'''玩家角色类'''
	def __init__(self,cid,name=u'',dynamicId=-1,status=1):
		'''构造方法
		@dynamicId (int) 角色登录的动态ID socket连接产生的id
		'''
		Character.__init__(self,cid,name)
		self.setCharacterType(Character.GAMERTYPE)#设置角色类型为玩家角色
		self.dynamicId=dynamicId #角色登录服务器时的动态id
		#-----------角色的各个组件类----------------
		self.level=CharacterLevelComponent(self) #角色等级
		self.finance=CharacterFinanceComponent(self) #角色资产
		self.pack=CharacterPackageComponent(self) #角色包裹
		self.attribute=CharacterAttributeComponent(self) #角色属性
		self.mail=CharacterMailListComponent(self)#角色邮件列表
		self.playerInner=PlayerInner(self)#球员找寻
		self.player=PlayerComponent(self)#球队球员
		self.zen=CharacterZenComponent(self)#球队战术
		self.shop=CharacterShopComponent(self)#商店
		self.task=CharacterTaskComponent(self)#任务
		self.trainmatch=TrainMatchComponent(self)#训练赛
		self.challengematch=ChallengeMatchComponent(self)#挑战赛
		if status:
			self.initGamerInfo() #初始化角色

	def initGamerInfo(self):
		'''初始化角色信息'''
		cid=self.baseInfo.id
		charactermode=tb_character_admin.getObj(cid)
		data=charactermode.get("data")
		if not data:
			print "Inint_gamer _"+str(self.baseInfo.id)
		#---------初始化角色基础信息组件---------
		self.baseInfo.setType(data['viptype']) #角色VIP类型
		self.baseInfo.setnickName(data['nickname']) #角色昵称
		#---------初始化角色经验等级组件---------
		self.level.setLevel(data['level'])
		self.level.setExp(data['exp'])
		self.level.setVipExp(data['vipexp'])
		#---------初始化角色属性信息组件---------
		self.attribute.initEnergy(data['energy'])
		self.attribute.setPhoto(data['Photo'])
		self.attribute.setPower(data['power'])
		self.attribute.setMaxPower(data['maxpower'])
		self.attribute.setTrainPoint(data['trainpoint'])
		self.attribute.setTacticsPoint(data['tacticspoint'])
		self.attribute.setRepute(data['repute'])#角色声望
		#---------初始化角色资产信息组件---------
		self.finance.setGameCoin(data['gamecoin'])
		self.finance.setCoin(data['coin'])
		#---------初始化包裹---------------------
		self.pack.initPack(packageSize=data['packageSize'])
		#---------初始化角色球员信息-------------
		self.player.initPlayerInfo()
		#---------初始化角色任务-----------------
		self.task.initCharacterTask()

	def getDynamicId(self):
		'''获取角色的动态Id'''
		return self.dynamicId

	def formatInfo(self):
		'''格式化角色基本信息'''
		characterInfo={}
		characterInfo['id']=self.baseInfo.id #角色的ID
		characterInfo['nickname']=self.baseInfo.getNickName()#角色的昵称
		characterInfo['roletype']=self.baseInfo.getType()#角色V类型
		characterInfo['vipexp']=self.level.getVipExp()#VIP经验
		characterInfo['level']=self.level.getLevel()#等级
		characterInfo['energy']=self.attribute.getEnergy()#活力
		characterInfo['photo']=self.attribute.getPhoto()
		characterInfo['power']=self.attribute.getPower()
		characterInfo['maxpower']=self.attribute.getMaxPower()
		characterInfo['trainpoint']=self.attribute.getTrainPoint()
		characterInfo['repute']=self.attribute.getRepute()#声望
		characterInfo['exp']=int(self.level.getExp())#经验
		characterInfo['maxExp']=int(self.level.getMaxExp())#最大经验
		characterInfo['gamecoin']=self.finance.getGameCoin()#银币
		characterInfo['coin']=self.finance.getCoin()#金币
		characterInfo['zenid']=self.zen.getZenId()
		characterInfo['tacticspoint']=self.attribute.getTacticsPoint()
		return characterInfo

	def CheckClient(self,dynamicId):
		'''检查客户端id是否匹配'''
		if self.dynamicId==dynamicId:
			return True
		return False

	def updateGamerDBInfo(self):
		'''更新角色在数据库中的数据'''
		cid=self.baseInfo.id
		pmmode=tb_character_admin.getObj(cid)
		mapping={'level':self.level.getLevel(),'repute':self.attribute.getRepute(),'gamecoin':self.finance.getGameCoin(),'coin':self.finance.getCoin(),'exp':self.level.getExp(),'energy':self.attribute.getEnergy(),'trainpoint':self.attribute.getTrainPoint(),'power':self.attribute.getPower(),'maxpower':self.attribute.getMaxPower(),'tacticspoint':self.attribute.getTacticsPoint()}
		pmmode.update_multi(mapping)

	def CalPower(self):
		'''计算球队实力'''
		zen=self.zen.getZenInfo()
		zenid=zen.get('zenId')
		zenlv=0
		if zenid==1:
			zenlv=zen.get('lvzen1')
		elif zenid==2:
			zenlv=zen.get('lvzen2')
		elif zenid==3:
			zenlv=zen.get('lvzen3')
		elif zenid==4:
			zenlv=zen.get('lvzen4')
		elif zenid==5:
			zenlv=zen.get('lvzen5')
		elif zenid==6:
			zenlv=zen.get('lvzen6')
		power=self.attribute.calClubPower(zenid,zenlv)
		return power

	def getZenId(self):
		''''''
		return self.zen.getZenId()
