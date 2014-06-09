#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.game.component.Component import Component
from app.game.core.pack import Package
from app.game.core.Item import Item
import copy,random
from app.share.dbopear import dbItems
from app.dbfront.memmode import tb_item_admin
from app.game import util


MAX_STACK=999

class CharacterPackageComponent(Component):
	'''角色的包裹组件
	'''

	def __init__(self,owner):
		'''初始化玩家包裹组件
		@param _package: Package object 包裹栏
		'''
		Component.__init__(self,owner)
		self._package=None
		self._tempPackage=None

	def initPack(self,packageSize=50):
		'''初始化包裹'''
		self.setPackage(size=packageSize)

	def getPackage(self):
		'''返回角色包裹信息'''
		return self._package

	def setPackage(self,size=12):
		'''读取数据库设置角色包裹
		@param size:int 包裹的大小
		'''
		self._package=Package.Package(size)
		itemlist=tb_item_admin.getAllPkByFk(self._owner.baseInfo.id)
		itemobjlist=tb_item_admin.getObjList(itemlist)
		for itemmode in itemobjlist:
			itemId=int(itemmode._name.split(':')[1])
			item = Item(id=itemId)
			itemPackInfo=itemmode.get('data')
			item.initItemInstance(itemPackInfo)
			self._package.putItemInPackage(item)

	def putNewItemInPackage(self,item):
		'''放置一个新的物品到包裹栏中
		@param item: item Object 物品实例
		@param position: int 物品的位置
		@param packageType: int 包裹的类型
		@param truner: int 是否是翻牌子获取的
		'''
		package=self._package
		maxstack=item.baseInfo.getItemTemplateInfo().get('maxstack',1)
		if maxstack>1:
			nowstack=item.pack.getStack()
			templateId=item.baseInfo.getItemTemplateId()
			state=0
			for _item in package.getItems().values():
				if _item.baseInfo.getItemTemplateId()==templateId:
					_item.pack.updateStack(_item.pack.getStack()+nowstack)
					state=1
					break
			if not state:
				if item.baseInfo.getId()==0:
					item.InsertItemIntoDB(characterId=self._owner.baseInfo.id)
				package.putItemInPackage(item)
		else:
			if item.baseInfo.getId()==0:
				item.InsertItemIntoDB(characterId=self._owner.baseInfo.id)
			package.putItemInPackage(item)
		return 2

	def putNewItemsInPackage(self,itemTemplateId,count):
		'''添加物品到包裹栏'''
		item=Item(itemTemplateId=itemTemplateId)
		maxstack=item.baseInfo.getItemTemplateInfo().get('maxstack',1)
		itemcndlist=[]
		if maxstack>1:
			while count>MAX_STACK:
				count-=MAX_STACK
				itemcndlist=[MAX_STACK]
			if count>0:
				itemcndlist.append(count)
		else:
			itemcndlist=[1]*count
		for count in itemcndlist:
			_item=copy.deepcopy(item)
			_item.pack.setStack(count)
			self.putNewItemInPackage(_item)
		return True

	def countItemTemplateId(self,TemplateId):
		'''判断是否存在物品'''
		package = self._package
		count=package.countItemTemplateId(TemplateId)
		return count 

	def delItemByTemplateId(self,templateId,count):
		'''根据物品的模板id删除物品
		@param templateId: int 模板的id
		@param count: int 物品的数量
		'''
		package=self._package
		if self.countItemTemplateId(templateId)<count:
			return -1 # 数量不足
		for itemid,item in package.getItems().items():
			if item.baseInfo.itemTemplateId!=templateId:
				continue
			if count==0:
				break
			nowstack=item.pack.getStack()
			if nowstack>=count:
				package.deleteitemById(itemid,count=count)
				break
			else:
				package.deleteitemById(itemid,count= -1)
				count -= nowstack
		return 1#成功

	def delItemByItemId(self,itemId,count=1):
		'''根据物品的id删除物品
		@param itemId: int 物品的id
		@param count: int 物品的数量
		'''
		package=self._package.getPropsPagePack()
		result=package.deleteitemById(itemId,count=count)
		return result#成功

	def useItem(self,itemid,targetid):
		'''使用物品
		@param itemid: int 物品的id
		@param targetid: int 目标id，默认为0
		'''
		item=self._package.getItemById(itemid)
		if not item:
			return {'result':False,'message':u"1"}
		script=item.baseInfo.getUseScript()#物品使用的脚本
		if not script:
			return {'result':False,'message':"2"}
		# if item.baseInfo.getLevelRequired()>self._owner.level.getLevel():
		# 	return {'result':False,'message':"等级不足"}
		try:
			exec(script)#执行任务脚本
		except Exception,e:
			return {'result':False,'message':e.message}
		self.delItemByItemId(itemid,1)
		return {'result':True,'message':""}

	def openChest(self,itemsInfolist,default,requiredItem,requiredCount):
		'''开启宝箱
		@param itemsInfo:list [(物品ID，物品数量，随机取件)]随机掉落
		@param default: (物品ID,物品数量)默认掉落
		@param requiredItem:int 需要消耗的物品的模板ID
		@param requiredCount: int 需要消耗的物品的数量
		'''
		if requiredItem!=0:
			count=self._owner.pack.countItemTemplateId(requiredItem)
			iteminfo=dbItems.all_ItemTemplate.get(requiredItem)
			if count<requiredCount:
				raise Exception(u'%s数量不足'%iteminfo.get('name'))
		itemsrates=[item[2] for item in itemsInfolist]
		iteminfo=None
		rate=random.randint(0,RATE_BASE)
		for index in range(len(itemsInfolist)):
			if rate<sum(itemsrates[:index+1]):
				iteminfo=itemsInfolist[index]
				break
		if not iteminfo:
			iteminfo=default
		result=self.putNewItemsInPackage(iteminfo[0],iteminfo[1])
		if not result:
			raise Exception("")
		self.delItemByTemplateId(requiredItem,requiredCount)

	def HuoQuSuiPianBaoguo(self):
		'''获取包裹中的碎片信息
		'''
		suipianList=[]#碎片列表
		for i_item in self._package.getItems().values():
			itemTempinfo=i_item.baseInfo.getItemTemplateInfo()
			if itemTempinfo.get('compound',0):
				info={}
				info['itemid']=i_item.baseInfo.id
				info['icon']=itemTempinfo.get('icon',0)
				info['tempid']=itemTempinfo.get('id',0)
				info['stack']=i_item.pack.getStack()
				suipianList.append(info)
		return {'result':True,'data':{'itemlist':suipianList}}

	def CompoundItem(self,itemId):
		'''合成物品
		'''
		suipianinfo=dbItems.all_ItemTemplate.get(itemId)
		if not suipianinfo:
			return {'result':False,'message':u"碎片信息不存在"}
		gamecoinrequired=suipianinfo.get('comprice',0)
		if gamecoinrequired>self._owner.finance.getGameCoin():
			return {'result':False,'message':u"银币不足"}

		newtempid=suipianinfo.get('compound',0)
		newiteminfo=dbItems.all_ItemTemplate.get(newtempid)
		if not newiteminfo:
			return {'result':False,'message':u"该物品不能合成"}
		itemrequired=self._package.countItemTemplateId(itemId)
		if itemrequired<5:
			return {'result':False,'message':u"缺少材料"}
		self._owner.finance.addGameCoin(-gamecoinrequired)
		self.delItemByTemplateId(itemId,5)
		newiteminfo=dbItems.all_ItemTemplate.get(newtempid)
		self.putNewItemsInPackage(newtempid,1)
		return {'result':True,'message':u"合成成功"}

	def getPackageItemList(self):
		'''获取包裹的物品信息
		'''
		data={}
		itemList=self._package._items.values()
		data['itemlist']=[{'itemid':itemInfo.baseInfo.id,'tempinfo':itemInfo.baseInfo.getItemTemplateInfo(),'stack':itemInfo.pack.getStack()} for itemInfo in itemList]
		return {'result':True,'data':data}







