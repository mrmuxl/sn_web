#_*_coding:utf-8_*_

import datetime,logging,json
from django.conf import settings
from models import VIPUser,Print,Shared,PrintAccess,SharedAccess
from apps.kx.models import KxUserFriend
from apps.kx.models import KxUser
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_POST,require_GET)
from django.http import HttpResponseRedirect,HttpResponse
from apps.kx.utils import is_valid_email,send_mail_thread
from django.utils.html import strip_tags
from mail_text import vipuser_tip
from pprint import pprint

logger = logging.getLogger(__name__)

def access_user_print(email):
    message = {}
    now = datetime.datetime.now()
    print_access_list = []
    try:
        print_user = Print.objects.filter(expire__gt=now).select_related().get(email=email)
        if print_user:
            message['is_print']= print_user.is_print #为打印共享用户
            if print_user.is_print:
                message['remainder_print_num']= (print_user.print_num - print_user.used_print_num)
            else: 
                message['remainder_print_num']= -1 #不能授权
            print_access_obj_set = print_user.print_access.filter(status=1)
            if print_access_obj_set:
                for i in print_access_obj_set:
                    print_access_list.append(i.access_user_id)
                    #print_access_list.append({"email":i.access_user_id})
            message['print_access_user']=print_access_list
            logger.info("access_user_print_message:%s",message)
    except Exception as e:
        logger.debug("print_user:%s",e)
        print_access_user_set = Print.objects.filter(print_access__access_user=email).filter(expire__gt=now).filter(print_access__status=1)
        logger.info("print_access:%s",print_access_user_set)
        is_print =False
        if print_access_user_set:
            for i in print_access_user_set:
                if i.is_print:
                    is_print = True
        message['is_print']= is_print 
        message['remainder_print_num']= -1
        message['print_access_user']=print_access_list
        logger.info("print_access_user_set_message:%s",message)
    return message

def access_user_shared(email):
    message = {}
    now = datetime.datetime.now()
    shared_access_list =[]
    try:
        shared_user = Shared.objects.filter(expire__gt=now).select_related().get(email=email)
        if shared_user:
            message['is_shared']= shared_user.is_shared #为文件共享用户
            if shared_user.is_shared:
                message['remainder_shared_num']= (shared_user.shared_num - shared_user.used_shared_num)
            else:
                message['remainder_shared_num']= -1
            shared_access_obj_set = shared_user.shared_access.filter(status=1)
            if shared_access_obj_set:
                for i in shared_access_obj_set:
                    shared_access_list.append(i.access_user_id)
            message['shared_access_user']=shared_access_list
            logger.info("access_user_shared_message:%s",message)
    except Exception as e:
        logger.debug("shared_user:%s",e)
        shared_access_user_set = Shared.objects.filter(shared_access__access_user=email).filter(expire__gt=now).filter(shared_access__status=1)
        logger.info("shared_access_user_set:%s",shared_access_user_set)
        is_shared = False
        if shared_access_user_set:
            for i in shared_access_user_set:
                if i.is_shared:
                    is_shared = True
        message['is_shared']= is_shared 
        message['remainder_shared_num']= -1 #不能授权
        message['shared_access_user']=shared_access_list
        logger.info("shared_access_user_set_message:%s",message)
    return message
 
