#!/usr/bin/python2
#-*- coding:utf-8 -*-
import MySQLdb
import logging

logger = logging.getLogger(__name__)
conn = MySQLdb.connect(host='localhost',user='root',passwd='mrmuxl',db='kx')
with conn:
    cursor = conn.cursor()
    #字典游标
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select email from publish_user" )
    publish_user = cursor.fetchall()
    sql="""insert into publish_user values(%(id)s,%(email)s,%(ver)s,%(repo_ver)s,%(is_publish)s)"""
    for i in publish_user:
        if not i['email'] == 'simplenect@simplenect.com':
            cursor.execute("select * from publish_user where email=%s",i['email'])
            publish_info = cursor.fetchone()
            print "publish info:%s" %(publish_info)
            cursor.execute("select friend from kx_user_friend where user=%s",(i['email']))
            friends = cursor.fetchall()
            print "%s's friends:%s" %(i['email'],friends)
            for f in friends:
                try:
                    f.update({"id":None,"email":f['friend'],"ver":publish_info['ver'],"repo_ver":publish_info['repo_ver'],"is_publish":publish_info['is_publish']})
                    cursor.execute(sql,f)
                    print "insert:%s" %(f)
                except Exception as e:
                    logger.debug("%s",e)
                    print "inster exception:%s" %e
            print "update %s rows" %(cursor.rowcount)
    cursor.close()
