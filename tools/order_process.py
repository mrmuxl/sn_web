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

def get_all_order(cursor):
    order_sql="""select order_id,buy_user,buy_product_id,auth_user_num,total_fee from order_info where pay_status=1 and status =0"""
    order = fetchall(order_sql,cursor)
    print "get_all_order:",order
    return order

def get_product(cursor,pid):
    product_sql ="""select category,price from product_info where id=%(id)s"""
    data ={"id":pid}
    one_line = fetchone(product_sql,cursor,data=data)
    return one_line

def get_print(cursor,email):
    print_sql ="""select * from print where email=%(email)s"""
    email ={"email":email}
    one_print = fetchone(print_sql,cursor,data=email)
    return one_print

def get_shared(cursor,email):
    sql ="""select * from shared where email=%(email)s"""
    email ={"email":email}
    one_shared = fetchone(sql,cursor,data=email)
    return one_shared

def get_vip(cursor,email):
    sql ="""select * from vipuser where email=%(email)s"""
    values ={'email':email}
    one_vip = fetchone(sql,cursor,data=values)
    return one_vip

def insert_print(cursor,email,print_num,create_at,expire):
    sql="""insert into print values(%(id)s,%(email)s,%(is_print)s,%(print_num)s,%(used_print_num)s,%(create_at)s,%(expire)s)"""
    data={"id":None,"email":email,"is_print":True,"print_num":print_num,"used_print_num":0,"create_at":create_at,"expire":expire}
    try:
        cursor.execute(sql,data)
        print "insert print successful:",data
        return True
    except Exception as e:
        print "execute error",e
        return False
    
def insert_shared(cursor,email,shared_num,create_at,expire):
    sql="""insert into shared values(%(id)s,%(email)s,%(is_shared)s,%(shared_num)s,%(used_shared_num)s,%(create_at)s,%(expire)s)"""
    data={"id":None,"email":email,"is_shared":True,"shared_num":shared_num,"used_shared_num":0,"create_at":create_at,"expire":expire}
    try:
        cursor.execute(sql,data)
        print "insert shared successful:",data
        return True
    except Exception as e:
        print "insert shared execute error",e
        return False

def insert_vip(cursor,email,create_at,expire):
    sql="""insert into vipuser values(%(id)s,%(email)s,%(is_vip)s,%(create_at)s,%(expire)s)"""
    data={"id":None,"email":email,"is_vip":True,"create_at":create_at,"expire":expire}
    try:
        cursor.execute(sql,data)
        print "insert vip successful:",data
        return True
    except Exception as e:
        print "insert vip execute error",e
        return False

def update_print(cursor,email,print_num,expire):
    sql="""update print set is_print=%(is_print)s,print_num=%(print_num)s, expire = %(expire)s where email=%(email)s"""
    data = {"email":email,"is_print":True,"print_num":print_num,"expire":expire}
    try:
        cursor.execute(sql,data)
        print "update_print successful:",data
        return True
    except Exception as e:
        print "update print execute error",e
        return False

def update_shared(cursor,email,print_num,expire):
    sql="""update shared set is_shared=%(is_shared)s,shared_num=%(shared_num)s, expire = %(expire)s where email=%(email)s"""
    data = {"email":email,"is_shared":True,"shared_num":shared_num,"expire":expire}
    try:
        cursor.execute(sql,data)
        print "update_shared:",data
        return True
    except Exception as e:
        print "update shared execute error",e
        return False

def update_vip(cursor,email,expire):
    sql="""update vipuser set is_vip=1, expire = %(expire)s where email=%(email)s"""
    data = {"email":email,"expire":expire}
    try:
        cursor.execute(sql,data)
        print "update_vip:",data
        return True
    except Exception as e:
        print "update vip execute error",e
        return False

def update_order(cursor,order_id):
    sql="""update order_info set status = 1 where order_id=%(order_id)s"""
    data = {"order_id":order_id}
    try:
        cursor.execute(sql,data)
        print "update order_info successful!",order_id
        return True
    except Exception as e:
        print "update order_info execute error",e
        return False

def new_month(month):
    if month >= 6 and month < 12:
        month+=1
    if month >= 12:
        month+=2
    return month

def get_month_days(year, month):
    MONTH_DAYS = [0,31,28,31,30,31,30,31,31,30,31,30,31];
    if(month==2):
        if(((year%4 == 0) and (year%100 != 0)) or (year%400 == 0)):
            return 29
        else:
            return 28
    else:
        return (MONTH_DAYS[month])

def set_expire(now,month,expire=None):
    if expire is not None and expire > now:
        m = expire.month + month
        y = expire.year
        d = expire.day
        while m > 12:
            m -=12
            y += 1
        days = get_month_days(y,m)
        if d > days:
            m += 1
            d -= days
        t = datetime(y,m,d)
    else:
        m = now.month + month
        y = now.year
        d = now.day
        while m > 12:
            m -= 12
            y += 1
        days = get_month_days(y,m)
        if d > days:
            m += 1
            d -= days
        t = datetime(y,m,d)
    return t


if __name__ == '__main__':
    now = datetime.now()
    print now
    try:
        conn = get_conn('localhost','root','abc123!!','kx')
    except Exception as e:
        conn = get_conn('localhost','root','mrmuxl','kx')
    cursor = init_cursor(conn)
    all_order = get_all_order(cursor)
    if all_order:
        for i in all_order:
            print i
            pdt = get_product(cursor,i['buy_product_id'])
            if  pdt['category'] == 1:
                m = int(i['total_fee']/50)
                month = new_month(m)
                one_print = get_print(cursor,i['buy_user'])
                one_shared = get_shared(cursor,i['buy_user'])
                one_vip = get_vip(cursor,i['buy_user'])
                try:
                    if one_print:
                        expire = set_expire(now,month,one_print['expire'])
                        print "p",expire
                        print_num = 999
                        update_print(cursor,i['buy_user'],print_num,expire)
                    else:
                        expire = set_expire(now,month)
                        print "pr",expire
                        print_num = 999
                        insert_print(cursor,i['buy_user'],print_num,now,expire)
                    if one_shared:
                        expire = set_expire(now,month,one_shared['expire'])
                        print "s",expire
                        shared_num = 999
                        update_shared(cursor,i['buy_user'],shared_num,expire)
                    else:
                        expire = set_expire(now,month)
                        print "sd",expire
                        shared_num = 999
                        insert_shared(cursor,i['buy_user'],shared_num,now,expire)
                    if one_vip:
                        expire = set_expire(now,month,one_shared['expire'])
                        print "vip",expire
                        update_vip(cursor,i['buy_user'],expire)
                    else:
                        expire = set_expire(now,month)
                        print "vipd",expire
                        insert_vip(cursor,i['buy_user'],now,expire)
                    update_order(cursor,i['order_id'])
                except Exception as e:
                    print "vip process",e
            elif pdt['category'] == 2:
                m = int((i['total_fee']-i['auth_user_num']*5)/15)
                month = new_month(m)
                one_print = get_print(cursor,i['buy_user'])
                if one_print:
                    expire = set_expire(now,month,one_print['expire'])
                    print_num = one_print['print_num'] + i['auth_user_num']
                    update_print(cursor,i['buy_user'],print_num,expire)
                    update_order(cursor,i['order_id'])
                else:
                    expire = set_expire(now,month)
                    print_num = 5 + i['auth_user_num']
                    insert_print(cursor,i['buy_user'],print_num,now,expire)
                    update_order(cursor,i['order_id'])
            elif pdt['category'] == 4:
                m = int((i['total_fee']-i['auth_user_num']*5)/15)
                month = new_month(m)
                one_shared = get_shared(cursor,i['buy_user'])
                if one_shared:
                    expire = set_expire(now,month,one_shared['expire'])
                    shared_num = one_shared['shared_num'] + i['auth_user_num']
                    update_shared(cursor,i['buy_user'],shared_num,expire)
                    print "update shared"
                    update_order(cursor,i['order_id'])
                else:
                    expire = set_expire(now,month)
                    shared_num = 5 + i['auth_user_num']
                    insert_shared(cursor,i['buy_user'],shared_num,now,expire)
                    print "instert shared"
                    update_order(cursor,i['order_id'])
            else:
                print "no category"
    cursor.close()
    print "cursor close"
    conn.commit()
    conn.close()
    print "conn close"
