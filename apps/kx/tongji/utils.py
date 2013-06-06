#_*_coding:utf-8_*_

from django.db import connection
import logging

logger = logging.getLogger(__name__)

class CustomSQL(object):
    def __init__(self,q=None,p=[]):
        self.q = q
        self.p = p
        self.cursor = connection.cursor()
    def fetchone(self):
        self.cursor.execute(self.q,self.p)
        row = self.cursor.fetchone()
        return row
    def fetchall(self):
        self.cursor.execute(self.q,self.p)
        rows= self.cursor.fetchall()
        return rows



def bug_chart_sql(q=None,p=[]):
    try:
        A_tuple = CustomSQL(q=q,p=p).fetchall()
        A_list = []
        if len(A_tuple) < 30:
            for i in range(30):
                try:
                    A_list.append(A_tuple[i][0])
                except Exception as e:
                    A_list.append(0)
                    pass
        else:
            A_list = [i[0] for i in A_tuple]
        return A_list
    except Exception as e:
        logger.debug("%s",e)
        return A_list
