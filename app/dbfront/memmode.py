#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''
from gfirefly.dbentrust.mmode import MAdmin

tb_character_admin=MAdmin('tb_character','id',incrkey='id')
tb_character_admin.insert()
tb_player_admin=MAdmin('tb_player','id',fk='cid',incrkey='id')
tb_player_admin.insert()
tb_item_admin=MAdmin('tb_item','id',fk='characterId',incrkey='id')
tb_item_admin.insert()
tb_zen_admin=MAdmin('tb_character_zen','characterId',incrkey='id')
tb_zen_admin.insert()