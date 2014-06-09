#coding:utf8
'''
Created on 2014-1-26

@author: CC
'''
from gfirefly.dbentrust.dbpool import dbpool
from MySQLdb.cursors import DictCursor
from gfirefly.dbentrust import util

PLAYER_EXP={}
PLAYER_TEMPLATE = {}#球员模板表
PLAYER_TEMPLATE_FINDABLE={}
PLAYER_TEMPLATE_BEGIN={}

def UpdatePlayerInfo(playerId,props):
	'''更新球员信息'''
	sqlstr=util.forEachUpdateProps('tb_player',props,{'id':playerId})
	conn=dbpool.connection()
	cursor=conn.cursor()
	count=cursor.execute(sqlstr)
	conn.commit()
	cursor.close()
	conn.close()
	if count>=1:
		return True
	else:
		return False

def getPlayerExp():
	'''获取球员的经验表'''
	global PLAYER_EXP
	sql="select * from tb_player_experience"
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchall()
	cursor.close()
	conn.close()
	for exp in result:
		PLAYER_EXP[exp['quality']]={1:exp['lv1'],2:exp['lv2'],3:exp['lv3'],4:exp['lv4'],5:exp['lv5'],6:exp['lv6'],7:exp['lv7'],8:exp['lv8'],9:exp['lv9']}

def getAllPlayerTemplate():
	'''获取球员的模板信息'''
	global PLAYER_TEMPLATE
	sql="SELECT * FROM tb_player_template"
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchall()
	cursor.close()
	conn.close()
	for player in result:
		PLAYER_TEMPLATE[player['id']]=player

def getFindPlayerTemplateByLeague(leagueindex):
	'''获取球员的模板信息'''
	global PLAYER_TEMPLATE_FINDABLE
	players={}
	sql="SELECT a.* FROM tb_player_template a inner join tb_npcclub b on a.tClubID=b.ID WHERE a.findable=1 and b.LeagueIndex=%d"%leagueindex
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchall()
	cursor.close()
	conn.close()
	conn.close()
	for player in result:
		players[player['id']]=player
	PLAYER_TEMPLATE_FINDABLE[leagueindex]=players

def getInitPlayer():
	'''获取初始球员的模板信息'''
	global PLAYER_TEMPLATE
	sql="SELECT * FROM tb_player_template WHERE `tClubID`=1001"
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchall()
	cursor.close()
	conn.close()
	for player in result:
		PLAYER_TEMPLATE_BEGIN[player['id']]=player