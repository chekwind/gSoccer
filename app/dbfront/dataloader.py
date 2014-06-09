#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

import memmode
from gfirefly.dbentrust.madminanager import MAdminManager
from gtwisted.core import reactor
reactor=reactor

def registe_madmin():
	'''
	'''
	MAdminManager().registe(memmode.tb_character_admin)
	MAdminManager().registe(memmode.tb_player_admin)
	MAdminManager().registe(memmode.tb_item_admin)
	MAdminManager().registe(memmode.tb_zen_admin)

def CheckMemDB(delta):
	'''
	'''
	MAdminManager().checkAdmins()
	reactor.callLater(delta,CheckMemDB,delta)