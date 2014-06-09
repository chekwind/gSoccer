#coding:utf8
'''
Created on 2014-3-20

@author: CC
'''

from flask import request
from memmode import register_admin
from gfirefly.server.globalobject import GlobalObject,webserviceHandle
from urls import getDayRecordList,getStatistics
import json

@webserviceHandle('/opera')
def operaGamer():
	username=request.args['username']
	opera_str=request.args['opera_str']
	usermodedata=register_admin.getObjData(username)
	if not usermodedata:
		return "Account dose not exist!!!"
	pid=usermodedata.get('id')
	if not pid:
		return "Role does not exist!!!"
	gate_node=GlobalObject().remote.get('gate')
	gate_node.callRemote("opera_gamer",pid,opera_str)
	return "Success"

@webserviceHandle('/dayrecored')
def dayrecord():
	'''获取每日的纪录'''
	index=int(request.args['index'])
	data=getDayRecordList(index)
	response=json.dumps(data)
	return response

@webserviceHandle('/statistics')
def Statistics():
	'''单服总数据统计'''
	data=getStatistics()
	response=json.dumps(data)
	return response