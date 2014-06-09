#coding:utf8
'''
Created on 2014-1-17

@author: CC
'''

from gfirefly.dbentrust.dbpool import dbpool
from gtwisted.utils import log
from gfirefly.dbentrust import util
from MySQLdb.cursors import DictCursor

def updateGamerInfo(characterId,props):
    ''''''
    sqlstr=util.forEachUpdateProps('tb_character',props,{'id':characterId})
    conn=dbpool.connection()
    cursor=conn.cursor()
    count=cursor.execute(sqlstr)
    conn.commit()
    cursor.close()
    conn.close()
    if count>=1:
		return True
    else:
        log.err(sqlstr)
        return False

def getAllInfo():
    '''获取所有角色信息'''
    sql="SELECT * FROM tb_character"
    conn=dbpool.connection()
    cursor=conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    conn.close()
    if data:
        return data
    return None

def updateDontTalk(cid,flg):
    '''更改角色禁言状态
    @param cid: int 角色id
    @param flg: int 0不禁言   1禁言
    '''
    sql="UPDATE  tb_character SET donttalk=%s WHERE id=%s"%(flg,cid)
    conn=dbpool.connection()
    cursor=conn.cursor()
    count = cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    if count>=1:
        return True
    return False

def getInfoByid(characterid):
    '''根据角色id获取角色信息'''
    sql="SELECT  id,nickname,`level` FROM tb_character WHERE id="+str(characterid)
    conn=dbpool.connection()
    cursor=conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    conn.close()
    if data:
        return data
    return None

def getCharacterIdByNickName(nickname):
    '''根据昵称获取角色的id
    @param nickname:string 角色的昵称
    '''
    sql="SELECT id from `tb_character` where nickname='%s'"%nickname
    conn=dbpool.connection()
    cursor=conn.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def getTop10(typeid):
    '''获取角色排行前10数据
    @param typeid: int 0等级 1实力 2 球员
    '''
    filedList=['cid','name','power']
    dt=[]
    od=""
    xs=""

    if typeid==0:
        od=" order by level desc,exp desc,id desc "
        xs=" nickname,level from tb_character "
    elif typeid==1:
        od=" order by maxpower desc "
        xs=" nickname,maxpower from tb_character "
    elif typeid==2:
        od="order by playerpower desc"
        xs="playername,playerpower from tb_player"

    sql="select "+xs+od
    sql+=" limit 0,10"
    conn=dbpool.connection()
    cursor=conn.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    for item in result:
        data={}
        for i in range(len(filedList)):
            data[filedList[i]]=item[i]
        dt.append(data)

    if not dt or len(dt)<1:
        return None
    return dt

