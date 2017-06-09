#_*_coding:utf-8_*_
"""执行原生SQL"""
import MySQLdb
from django.db import connection,transaction
def query_sql(sql,params=None):
    """
    ----------------------------------------------
    Function:    执行原始的SQL 查询操作
    DateTime:    2016/10/24
    ----------------------------------------------
    """
    cursor = connection.cursor() #获得一个游标(cursor)对象 
    if params is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql,params)
    return dictfetchall(cursor)             #返回dict 结果集   #返回结果行cursor.fetchone() 或使用 #raw = cursor.fetchall()

@transaction.commit_on_success
def execute_sql(sql,params=None):
    """更新操作"""
    cursor = connection.cursor()
    result=None
    if params is None:
        result=cursor.execute(sql)
    else:
        result=cursor.execute(sql,params)
    return result

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
