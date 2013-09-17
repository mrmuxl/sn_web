#!/usr/bin/python2
#-*- coding:utf-8 -*-
import MySQLdb
import logging
from pprint import pprint
from datetime import timedelta
from datetime import datetime

logger = logging.getLogger(__name__)

def get_conn(host,user,passwd,db):
    try:
        conn = MySQLdb.connect(host=host,user=user,passwd=passwd,db=db)
    except Exception as e:
        print "connection error",e
        raise
    return conn

def init_cursor(conn):
    cursor = conn.cursor()
    #字典游标
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    return cursor

def fetchall(sql,cursor,data=None):
    cursor.execute(sql,data)
    all =cursor.fetchall()
    return all
    
def fetchone(sql,cursor,data=None):
    cursor.execute(sql,data)
    one =cursor.fetchone()
    return one

def processlist(cursor):
    sql ="""show processlist"""
    all_list = fetchall(sql,cursor)
    return all_list



if __name__ == '__main__':
    now = datetime.now()
    print now
    try:
        conn = get_conn('localhost','root','abc123!!','kx')
    except Exception as e:
        conn = get_conn('localhost','root','mrmuxl','kx')
    cursor = init_cursor(conn)
    processlist = processlist(cursor)
    if processlist:
        for i in processlist:
            print i

    cursor.close()
    print "cursor close"
    conn.commit()
    conn.close()
    print "conn close"
