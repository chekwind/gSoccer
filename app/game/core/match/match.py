#coding:utf8
'''
Created on 2014-3-12

@author: CC
'''

from app.game.core.match.MatchSide import MatchSide
import random

HUIHE=20#回合数
MAXPROB=400#最大概率

class Match:
	'''比赛类'''
	def __init__(self,challenger,deffener):
		'''初始化比赛类'''
		self.challenger=challenger
		self.deffener=deffener

	def DoMatch(self):
		'''进行比赛'''
		self.challenger.attribute.calClubPower()
		self.deffener.attribute.calClubPower()
		chjingong,chzuzhi,chfangshou,chshoumen,chpower=self.challenger.attribute.getMatchData()
		dejingong,dezuzhi,defangshou,deshoumen,depower=self.deffener.attribute.getMatchData()
		chzenid=self.challenger.getZenId()
		dezenid=self.deffener.getZenId()
		chgong,chfang=self.calMatchData(chjingong,chzuzhi,chfangshou,chshoumen,chzenid)
		degong,defang=self.calMatchData(dejingong,dezuzhi,defangshou,deshoumen,dezenid)
		goalprob=chgong/defang
		loseprob=dejingong/chfangshou
		score=self.getMacthScore(goalprob*100,loseprob*100)
		return score


	def calMatchData(self,jingong,zuzhi,fangshou,shoumen,zenid):
		'''根据球队数据计算'''
		if zenid in(1,2):
			gong=jingong*0.5+zuzhi*0.5
			fang=fangshou*0.5+shoumen*0.5
		elif zenid in (3,4):
			gong=jingong*0.33+zuzhi*0.5
			fang=zuzhi*0.5+fangshou*0.33+shoumen*0.33
		elif zenid in (5,6):
			gong=jingong*0.5
			fang=zuzhi*0.33+fangshou*0.5+shoumen*0.5
		return gong,fang

	def getMacthScore(self,goalprob,loseprob):
		'''获取比赛结果'''
		if goalprob>MAXPROB:goalprob=MAXPROB
		if loseprob>MAXPROB:loseprob=MAXPROB
		offgoal,offlose,defgoal,deflose,offscore,defscore=0,0,0,0,0,0
		for i in range(HUIHE):
			s1=random.randint(0,1000)
			s2=random.randint(0,1000)
			s3=random.randint(0,1000)
			s4=random.randint(0,1000)
			if s1<=goalprob:
				offgoal+=1
			if s2<=loseprob:
				offlose+=1
			if s3<=loseprob:
				defgoal+=1
			if s4<=goalprob:
				deflose+=1
		if(offgoal-offlose)/2<0:
			defscore-=(offgoal-offlose)/2
		elif(defgoal-deflose)/2<0:
			offscore-=(defgoal-deflose)/2
		else:
			offscore=(offgoal-offlose)/2
			defscore=(defgoal-deflose)/2

		return offscore,defscore

def DoMatch(challenger,deffener):
	'''进行比赛'''
	match=Match(challenger,deffener)
	data=match.DoMatch()
	return data