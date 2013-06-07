
#_*_coding:utf-8_*_
import time,string,math,random

def uniqid():
    m = time.time()
    uniqid = '%8x%05x' %(math.floor(m),(m-math.floor(m))*1000000)
    valid_chars = list(set(string.hexdigits.lower()))
    entropy_string = ''
    for i in range(0,13,1):
        entropy_string += random.choice(valid_chars)
    uniqid = str_reverse(uniqid) + entropy_string
    return uniqid

def uniq():
    m = time.time()
    return '%8x' %(math.floor(m))
 
def str_reverse(s):
    return s[::-1]
    
