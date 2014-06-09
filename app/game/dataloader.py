#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from app.share.dbopear import dbShieldWord,dbPlayer,dbItems,dbTask,dbExperience,dbclub
from app.game.core.trainbase.TrainBase import TrainBase

def load_config_data():
	"""从数据库中读取配置信息
	"""
	dbShieldWord.getAll_ShieldWord()#载入关键字
	dbPlayer.getPlayerExp()#载入球员升级经验配置
	dbPlayer.getAllPlayerTemplate()#载入球员搜索模板
	for i in range(1,6):
		dbPlayer.getFindPlayerTemplateByLeague(i)
	dbPlayer.getInitPlayer()#载入初始球员模板
	dbItems.getAll_ItemTemplate()#载入道具模板
	dbTask.getALLTask()#载入任务
	dbExperience.getExperience_Config()#载入角色升级经验表
	trainbase=TrainBase()
	trainbase.initTrainBase()#初始化训练基地
	dbclub.getTrainMatchNPC()#初始化训练赛npc
	dbclub.getChallengeNpc()#初始化挑战赛npc

