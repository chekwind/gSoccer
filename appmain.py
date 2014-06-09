#coding:utf8

from gevent import monkey;monkey.patch_os()
import json,sys
reload(sys)
sys.setdefaultencoding('utf8')

from gfirefly.server.server import FFServer

if __name__=="__main__":
    args = sys.argv
    servername = None
    config = None
    if len(args)>2:
        servername = args[1]
        config = json.load(open(args[2],'r'))
    else:
        raise ValueError
    dbconf = config.get('db')
    memconf = config.get('memcached')
    sersconf = config.get('servers',{})
    masterconf = config.get('master',{})
    serconfig = sersconf.get(servername)
    ser = FFServer()
    ser.config(serconfig, servername=servername,dbconfig=dbconf, memconfig=memconf,masterconf=masterconf)
    ser.start()
    
    