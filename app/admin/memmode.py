#coding:utf8
'''
Created on 2014-3-20

@author: CC
'''

from gfirefly.dbentrust.mmode import MAdmin

register_admin=MAdmin('tb_character','nickname')
register_admin.insert()