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
    cursor.execute("select * from kx_msg_board where reply_id=0" )
    msg =cursor.fetchall()
    data = {}
    for i in msg:
        cursor.execute("select * from kx_user where uuid=%(uuid)s",{"uuid":i['user_id']})
        user = cursor.fetchone()
        cursor.execute("select * from kx_msg_board where reply_id=%(reply_id)s",{"reply_id":i['reply_id']})
        reply = cursor.fetchall()

        if user is None:
            user = {}
            user['id'] = 11

        sql="""insert into forum_post values(%(id)s,%(user_id)s,%(vote_up)s,%(vote_down)s,%(content)s,%(ip)s,%(status)s,%(created)s,%(modified)s,%(hits)s)"""
        data={"id":None,"user_id":user['id'],"vote_up":0,"vote_down":0,"content":i['msg'],"ip":i['ip'],"status":0,"created":i['create_time'],"modified":i['create_time'],"hits":0}
        print data
        cursor.execute(sql,data)
        for r in reply:
            print r
            sql="""insert into forum_comment values(%(id)s,%(fid_id)s,%(user_id)s,%(content)s,%(ip)s,%(status)s,%(created)s)"""
            data={"id":None,"user_id":user['id'],"fid_id":r['reply_id'],"content":r['msg'],"ip":r['ip'],"status":1,"created":r['create_time']}
            cursor.execute(sql,data)
            print data
    cursor.close()
