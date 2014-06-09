#coding:utf8
'''
Created on 2014-2-19

@author: CC
'''
from gfirefly.dbentrust.dbpool import dbpool
from MySQLdb.cursors import DictCursor

def getZenconfigRole(zenid,playerpos):
	'''根据战术ID和球员位置确定球员角色'''
	sql="select role from tb_zen_config where zenid=%d and playerpos='%s'"%(zenid,playerpos)
	conn=dbpool.connection()
	cursor=conn.cursor()
	cursor.execute(sql)
	result=cursor.fetchone()
	cursor.close()
	conn.close()
	role=0
	if result:
		role=result[0]
	return role