#coding:utf8
'''
Created on 2014-3-11

@author: CC
'''
from gfirefly.dbentrust.dbpool import dbpool
from MySQLdb.cursors import DictCursor
from app.game.core.Item import Item
from gtwisted.utils import log

TrainMatch_Dropout={}
Challenge_Dropout={}
BASERATE=100000

def getTrainMatchDropout():
	'''获取训练赛掉落信息'''
	global TrainMatch_Dropout
	sql="SELECT * FROM tb_dropout where category=7"
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchall()
	cursor.close()
	conn.close()
	if not result:
		return None
	for item in result:
		item['itemid']=eval("["+item['itemid']+"]")
		TrainMatch_Dropout[item['id']]=item

def getChallengeDropout():
	'''获取挑战赛掉落信息'''
	global Challenge_Dropout
	sql="SELECT * FROM tb_dropout where category=1"
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchall()
	cursor.close()
	conn.close()
	if not result:
		return None
	for item in result:
		item['itemid']=eval("["+item['itemid']+"]")
		Challenge_Dropout[item['id']]=item

def getDropByid(leagueindex,category):
	'''根据Leagueindex获取掉落物品信息
	@param leagueindex: int npc所在联盟
	@param category:int 比赛类型
	'''
	data={}
	if category==7:
		data=TrainMatch_Dropout.get(leagueindex,None)
	elif category==1:
		data=Challenge_Dropout.get(leagueindex,None)
	if not data:
		log.err(u'掉落表填写错误存在掉落信息－掉落主键：%d'%leagueindex)
		return None
	for item in data.get('itemid'):
		abss=random.randint(1,BASERATE)
		if abss>=1 and abss<=item[2]:
			abss=random.randint(1,itemid[1])
			item1=Item(item[0])
			item1.pack.setStack(abss)
			return item1
	return None

