#!/usr/bin/python2
#-*- coding:utf-8 -*-

import shutil
import os
import os.path
import sys

def cp60(args,dirname,filename):
    for i in filename:
        try:
            if i.startswith('snap_60X60_'):
                fn = i.replace('snap_60X60_','')
                src = dirname + '/' + i
                des= dirname+'/'+fn
                print 'from:%s   to:%s' %(src,des)
                shutil.copy2(src,des)
        except Exception as e:
            print "error,filename not startswith snap"
            pass
if len(sys.argv) > 1:
    os.path.walk(sys.argv[1],cp60,None)




