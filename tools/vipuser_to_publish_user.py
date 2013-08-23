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
    cursor.execute("select email from vipuser" )
    vipuser=cursor.fetchall()
    cursor.execute("select * from publish_user where email='simplenect@simplenect.com'")
    publish_info = cursor.fetchone()
    sql="""insert into publish_user values(%(id)s,%(email)s,%(ver)s,%(repo_ver)s,%(is_publish)s)"""
    for i in vipuser:
        print i
        if not i['email'] == 'simplenect@simplenect.com':
            try:
                i.update({"id":None,"email":i['email'],"ver":publish_info['ver'],"repo_ver":publish_info['repo_ver'],"is_publish":publish_info['is_publish']})
                cursor.execute(sql,i)
                print i
            except Exception as e:
                logger.info("%s",e)
                print e
    cursor.close()
