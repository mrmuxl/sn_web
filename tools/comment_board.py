#!/usr/bin/python2
#-*- coding:utf-8 -*-
import MySQLdb
import logging

logger = logging.getLogger(__name__)
conn = MySQLdb.connect(host='localhost',user='root',passwd='abc123!!',db='kx',charset="utf8")
with conn:
    cursor = conn.cursor()
    #字典游标
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from kx_msg_board where reply_id!=0 and is_del=0" )
    msg =cursor.fetchall()
    data = {}
    for i in msg:
        print i
        cursor.execute("select * from kx_user where uuid=%(uuid)s",{"uuid":i['user_id']})
        user = cursor.fetchone()
        if user is None:
            user['id'] = 11
        print user['id']
        sql="""insert into forum_comment values(%(id)s,%(fid_id)s,%(user_id)s,%(content)s,%(ip)s,%(status)s,%(created)s)"""
        data={"id":None,"user_id":user['id'],"fid_id":i['reply_id'],"content":i['msg'],"ip":i['ip'],"status":1,"created":i['create_time']}
        print data
        cursor.execute(sql,data)
    cursor.close()
