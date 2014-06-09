#coding:utf8
'''
Created on 2014-3-18

@author: CC
'''

from app.game.core.character.NPCClub import NPCClub

def GetNPCInfo(dynamicId,npcid):
	'''	获取npc球队信息'''
	npc=NPCClub(templateId=npcid,clubcategory=7)
	if not npc:
		return {'result':False,'message':u"角色不存在"}
	data=npc.getNPCPlayers()
	return {'result':True,'data':data}

# def GetNPCPower(dynamicId,npcid):
# 	'''	获取npc实力'''
# 	npc=NPCClub(templateId=npcid,clubcategory=7)
# 	if not npc:
# 		return {'result':False,'message':u""}
# 	data=npc.attribute.calClubPower()
# 	return {'result':True,'data':data}