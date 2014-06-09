#coding:utf8
'''
Created on 2014-2-26

@author: CC
'''

from gfirefly.dbentrust.dbpool import dbpool
from MySQLdb.cursors import DictCursor

TRAINMATCHNPC={}
CHALLENGENPC={}


def getTrainMatchNPC():
	'''获取训练赛NPC球队信息
	'''
	global TRAINMATCHNPC
	sql="SELECT * FROM tb_npcclub where clubcategory=7 order by leagueindex,clubpower"
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchall()
	cursor.close()
	conn.close()
	for npcclub in result:
		TRAINMATCHNPC[npcclub['ID']]=npcclub

def getChallengeNpc():
	'''获取挑战赛NPC球队信息
	'''
	global CHALLENGENPC
	sql="SELECT * FROM tb_npcclub where clubcategory=1 order by leagueindex,powerindex"
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchall()
	cursor.close()
	conn.close()
	for npcclub in result:
		CHALLENGENPC[npcclub['ID']]=npcclub

