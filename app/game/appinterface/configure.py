#coding:utf8
'''
Created on 2014-2-17

@author: CC
'''
import datetime,time

def m(m):
	'''分钟转秒数'''
	return m*60
def h(h):
	'''小时转秒'''
	return h*60*60
def date(d,h,m,s):
	'''返回秒数'''
	return d*24*3600+h*3600+m*60+s

def getchatimeTime(down,counts):
	'''获取两日期相差的时间，返回剩余秒数及其当前时间
	@param down: datetime 记录时间
	@param counts：int 间隔秒数
	'''
	nowtime=datetime.datetime.now()
	if not down:
		return [0,nowtime]

	lin=down
	b=datetime.timedelta(seconds=counts)
	lin=lin+b#记录时间+间隔秒数
	if lin>nowtime:#如果冷却时间不为0
		s1=(lin-nowtime).days
		s1=s1*24*3600
		s2=(lin-nowtime).seconds
		s=s1+s2
		return [s,nowtime]
	else:
		return [0,nowtime]

def getchaTime(down,counts):
	'''获取两日期相差的时间，返回剩余秒数
	@param down:datetime 记录时间
	@param counts:int 间隔秒数
	'''
	lin=datetime.datetime.strptime(str(down),'%Y-%m-%d %H:%M:%S.%f')
	nowtime=datetime.datetime.now()
	b=datetime.timedelta(seconds=counts)
	lin=lin+b
	if lin>nowtime:
		s1=(lin-nowtime).days
		s1=s1*24*3600
		s2=(lin-nowtime).seconds
		s=s1+s2
		return s
	else:
		return 0