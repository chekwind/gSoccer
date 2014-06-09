#coding:utf8
'''
Created on 2014-2-24

@author: CC
'''
from gfirefly.dbentrust.dbpool import dbpool
from MySQLdb.cursors import DictCursor

def getShopInfo(shopcategory):
	sql="select * from tb_shop where shopcategory=%d and begintime<now() and endtime>now()"%(shopcategory)
	conn=dbpool.connection()
	cursor=conn.cursor(cursorclass=DictCursor)
	cursor.execute(sql)
	result=cursor.fetchall()
	cursor.close()
	conn.close()
	return result