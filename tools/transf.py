#!/usr/bin/python2
#-*- coding:utf-8 -*-
import MySQLdb


conn = MySQLdb.connect(host='localhost',user='root',passwd='mrmuxl',db='kx')
conn1 = MySQLdb.connect(host='localhost',user='root',passwd='mrmuxl',db='kx5')

with conn:
    cursor = conn.cursor()
    cursor1=conn1.cursor()
    #字典游标
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #desc = cursor.description
    #print 'cur.description:',desc
    #cursor.execute('show tables')
    #tables = cursor.fetchall()
    #for i in tables:
    #    t = i[0]
    #    print t
    #    #cursor.execute("select * from %s limit 1" % t)
    cursor.execute("select * from kx_user" )
    user=cursor.fetchall()
    l =[]
    sql="""insert into kx_user values(%(password)s,%(last_login)s,%(is_superuser)s,%(id)s,%(email)s,%(nick)s,%(status)s,%(create_time)s,%(update_time)s,%(avatar)s,%(last_ip)s,%(mobile)s,%(department)s,%(login_status)s,%(qianmo_dot)s,%(con_qianmo_dot)s,%(invate_init)s,%(login_counts)s,%(create_group_counts)s,%(online_time)s,%(invites)s,%(user_share)s,%(share_begin_time)s,%(active_time)s,%(is_active)s,%(is_staff)s)"""
    #sql="""insert into kx_user(password,last_login,is_superuser,id,email,nick,status,create_time,update_time,avatar,last_ip,mobile,department,login_status,qianmo_dot,con_qianmo_dot,invate_init,login_counts,create_group_counts,online_time,invites,user_share,share_begin_time,active_time,is_active,is_staff) values(%(password)s,%(last_login)s,%(is_superuser)s,%(id)s,%(email)s,%(nick)s,%(status)s,%(create_time)s,%(update_time)s,%(avatar)s,%(last_ip)s,%(mobile)s,%(department)s,%(login_status)s,%(qianmo_dot)s,%(con_qianmo_dot),%(invate_init)s,%(login_counts)s,%(create_group_counts)s,%(online_time)s,%(invites)s,%(user_share)s,%(share_begin_time)s,%(active_time)s,%(is_active)s,%(is_staff)s)"""
    for i in user:
        i.update({"is_superuser":0,"is_active":1,"is_staff":0})
        #print i['create_time']
        if not i['create_time']:
            i['create_time']='0000-00-00 00:00:00'
        if not i['update_time']:
            i['update_time']='0000-00-00 00:00:00'
        if not i['last_login']:
            i['last_login']='0000-00-00 00:00:00'
        #l.append(i)
        print i
        cursor1.execute(sql,i)
    conn1.commit()




















##        email = i['email']
##        nick = i['nick']
##        password =i['password']
##        status=i['status']
##        create_time=i['create_time']
##        last_login=i['last_login']
##        update_time=i['update_time']
##        avatar=i['avatar']
##        last_ip=i['last_ip']
##        mobile=i['mobile']
##        department=i['department']
##        login_status=i['login_status']
##        qianmo_dot=i['qianmo_dot']
##        con_qianmo_dot=i['con_qianmo_dot']
##        invate_init=i['invate_init']
##        login_counts=i['login_counts']
##        create_group_counts=i['create_group_counts']
##        online_time=i['online_time']
##        invites=i['invites']
##        user_share=i['user_share']
##        share_begin_time=i['share_begin_time']
##        active_time=i['active_time']
#        print email,nick,password,status,create_time,last_login,update_time,avatar,last_ip,mobile,department,login_status,qianmo_dot,con_qianmo_dot,invate_init,login_counts,create_group_counts,online_time,invites,user_share,share_begin_time,active_time

    #l =[]
    #for i in user:
    #    param=(i[3],i[6],0,'',i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21],i[22])
    #    l.append(param)
    #cursor1.executemany(sql,l)
    cursor.close()
    #cursor1.close()

#if __name__ == '__main__':
