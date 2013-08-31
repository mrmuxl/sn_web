#_*_coding:utf-8_*_

import datetime,logging,json
from django.conf import settings
#from models import VIPUser,AccessVIPUser,AccessUser
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

@csrf_exempt
@require_POST
def vipuser_api(request):
    message = {}
    now = datetime.datetime.now()
    Dday = datetime.datetime(2013,8,10) #1944-06-06
    email = request.POST.get('email','')
    logger.info("email:%s",email)
    if email:
        friends=KxUserFriend.objects.filter(user=email).values('friend')
        vip_friends=VIPUser.objects.filter(is_vip__exact=1,expire__gt=now,email__in=friends).values('email')
        logger.info("friends:%s;vip_friends:%s" %(friends,vip_friends))
        ctime = KxUser.objects.filter(email=email).values('create_time')
        ctime = ctime[0]['create_time']
        if ctime >= Dday:
            remainder_days = (now - ctime).days
        else:
            remainder_days = (now - Dday).days
        try:
            vipuser_obj = VIPUser.objects.get(email=email)
            if vipuser_obj.is_vip:
                message['status']=1 #为VIP用户
                message['is_vip']=vipuser_obj.is_vip
                message['remainder_days']=-1 #不显示
                message['vip_friends']='not needed'
                message['is_print']= True #为打印共享用户
                message['is_shared']= True #为文件共享用户
                message['remainder_print_num']= -1
                message['remainder_shared_num']= -1
                message['access_user']=''
                if settings.DEBUG:
                    pprint(message)
                return HttpResponse(json.dumps(message),content_type="application/json")
            elif vip_friends:
                message['status']=2 #本身不为VIP用户,但是有VIP用户好友
                message['remainder_days']=-1
                message['is_vip']=False
                message['vip_friends']=list(vip_friends)
                message['is_print']= True #为打印共享用户
                message['is_shared']= True #为文件共享用户
                message['remainder_print_num']= -1
                message['remainder_shared_num']= -1
                message['access_user']=''
                if settings.DEBUG:
                    pprint(message)
                return HttpResponse(json.dumps(message),content_type="application/json")
            elif remainder_days <= 15:
                message['status']=1 #为VIP用户
                message['remainder_days']=(15-remainder_days) #显示剩余天数
                message['is_vip']=False
                message['vip_friends']='not needed'
                message['is_print']= True #为打印共享用户
                message['is_shared']= True #为文件共享用户
                message['remainder_print_num']= -1
                message['remainder_shared_num']= -1
                message['access_user']=''
                if settings.DEBUG:
                    pprint(message)
                return HttpResponse(json.dumps(message),content_type="application/json")
            else:
                try:
                    access_vip = AccessVIPUser.objects.filter(expire__gt=now).select_related().get(email=email)
                    access_user_list =[]
                    if access_vip:
                        message['status']=0 #无权限使用
                        message['remainder_days']=0
                        message['is_vip']=False
                        message['vip_friends']='no friends'
                        message['is_print']= access_vip.is_print #为打印共享用户
                        message['is_shared']= access_vip.is_shared #为文件共享用户
                        message['remainder_print_num']= (access_vip.print_num - access_vip.used_print_num)
                        message['remainder_shared_num']= (access_vip.shared_num - access_vip.used_shared_num)
                        access_obj_set = access_vip.access_user_email.all()
                        if access_obj_set:
                            for i in access_obj_set:
                                access_user_list.append(i.access_user_id)
                        message['access_user']=access_user_list
                        if settings.DEBUG:
                            pprint(message)
                        return HttpResponse(json.dumps(message),content_type="application/json")
                except Exception as e:
                    logger.debug("access_vip:%s",e)
                    try:
                        access_user_set = AccessVIPUser.objects.filter(access_user_email__access_user=email).filter(expire__gt=now)
                        if access_user_set:
                            aus= access_user_set[0]
                            message['status']=0 #无权限使用
                            message['remainder_days']=0
                            message['is_vip']=False
                            message['vip_friends']='no friends'
                            message['is_print']= aus.is_print #为打印共享用户
                            message['is_shared']= aus.is_shared #为文件共享用户
                            message['remainder_print_num']= (aus.print_num - aus.used_print_num)
                            message['remainder_shared_num']= (aus.shared_num - aus.used_shared_num)
                            message['access_user']=''
                            if settings.DEBUG:
                                pprint(message)
                            return HttpResponse(json.dumps(message),content_type="application/json")
                        else:
                            message['status']=0 #无权限使用
                            message['remainder_days']=0
                            message['is_vip']=False
                            message['vip_friends']='no friends'
                            message['is_print']= aus.is_print #为打印共享用户
                            message['is_shared']= aus.is_shared #为文件共享用户
                            message['remainder_print_num']= (aus.print_num - aus.used_print_num)
                            message['remainder_shared_num']= (aus.shared_num - aus.used_shared_num)
                            message['access_user']=''
                            if settings.DEBUG:
                                pprint(message)
                            return HttpResponse(json.dumps(message),content_type="application/json")
                    except Exception as e:
                        logger.debug("access_user:%s",e)
        except Exception as e:
            logger.debug("email not found:%s",e)
            if vip_friends:
                message['status']=2
                message['remainder_days']=-1
                message['is_vip']=False
                message['vip_friends']=list(vip_friends)
                message['is_print']= True #为打印共享用户
                message['is_shared']= True #为文件共享用户
                message['remainder_print_num']= -1
                message['remainder_shared_num']= -1
                message['access_user']=''
                if settings.DEBUG:
                    pprint(message)
                return HttpResponse(json.dumps(message),content_type="application/json")
            elif remainder_days <= 15:
                message['status']=1 #为VIP用户
                message['is_vip']=False
                message['remainder_days']=(15-remainder_days)
                message['vip_friends']='false'
                message['is_print']= True #为打印共享用户
                message['is_shared']= True #为文件共享用户
                message['remainder_print_num']= -1
                message['remainder_shared_num']= -1
                message['access_user']=''
                if settings.DEBUG:
                    pprint(message)
                return HttpResponse(json.dumps(message),content_type="application/json")
            else:
                try:
                    access_vip = AccessVIPUser.objects.filter(expire__gt=now).select_related().get(email=email)
                    access_user_list =[]
                    if access_vip:
                        message['status']=0 #无权限使用
                        message['remainder_days']=0
                        message['is_vip']=False
                        message['vip_friends']='no friends'
                        message['is_print']= access_vip.is_print #为打印共享用户
                        message['is_shared']= access_vip.is_shared #为文件共享用户
                        message['remainder_print_num']= (access_vip.print_num - access_vip.used_print_num)
                        message['remainder_shared_num']= (access_vip.shared_num - access_vip.used_shared_num)
                        access_obj_set = access_vip.access_user_email.all()
                        if access_obj_set:
                            for i in access_obj_set:
                                access_user_list.append(i.access_user_id)
                        message['access_user']=access_user_list
                        if settings.DEBUG:
                            pprint(message)
                        return HttpResponse(json.dumps(message),content_type="application/json")
                except Exception as e:
                    logger.debug("access_vip:%s",e)
                    try:
                        access_user_set = AccessVIPUser.objects.filter(access_user_email__access_user=email).filter(expire__gt=now)
                        if access_user_set:
                            is_print =False
                            is_shared =False
                            print_num =0
                            used_print_num = 0
                            shared_num = 0
                            used_shared_num = 0
                            for aus in access_user_set:
                                if aus.is_print:
                                    is_print = True
                                    print_num = aus.print_num
                                    use_print_num = aus.used_print_num
                                if aus.is_shared:
                                    is_shared =True
                                    shared_num = aus.shared_num
                                    used_shared_num = aus.used_shared_num
                            message['status']=0 #无权限使用
                            message['remainder_days']=0
                            message['is_vip']=False
                            message['vip_friends']='no friends'
                            message['is_print']= is_print #为打印共享用户
                            message['is_shared']= is_shared #为文件共享用户
                            message['remainder_print_num']= (print_num - used_print_num)
                            message['remainder_shared_num']= (shared_num - used_shared_num)
                            message['access_user']=''
                            if settings.DEBUG:
                                pprint(message)
                            return HttpResponse(json.dumps(message),content_type="application/json")
                        else:
                            message['status']=0 #无权限使用
                            message['remainder_days']=0
                            message['is_vip']=False
                            message['vip_friends']='no friends'
                            message['is_print']= False #为打印共享用户
                            message['is_shared']= False #为文件共享用户
                            message['remainder_print_num']= 0
                            message['remainder_shared_num']= 0
                            message['access_user']=''
                            if settings.DEBUG:
                                pprint(message)
                            return HttpResponse(json.dumps(message),content_type="application/json")
                    except Exception as e:
                        logger.debug("access_user:%s",e)
    else:
        message['message']='please post to me a email'
        message['status']="error"
        return HttpResponse(json.dumps(message),content_type="application/json")

@csrf_exempt
@require_GET
def vipuser_test(reqeust,ckey,email):
    key = '518279d14e20e'
    download_url =u'http://download.simplenect.cn/Install/SimpleNect_S3.3.6.2.zip' 
    from_email =u"SimpleNect"
    if ckey and email and key == ckey:
        email = strip_tags(email.strip().strip('/').lower())
        if not is_valid_email(email):
            message ="""邮箱格式不正确！<A HREF="javascript:history.back()">返 回</A>"""
        subject = u'SimpleNect文件仓库3.3.6.4版本发布！'
        msg = vipuser_tip(download_url)
        try:
            send_mail_thread(subject,msg,from_email,[email],html=msg)
            logger.info("email:%s",email)
        except Exception as e:
            logger.debug("%s",e)
        return HttpResponse(email+' is send ok')
    else:
        message = """Key Error or No email to send !<A HREF="javascript:history.back()">返 回</A>"""
        return HttpResponse(message)

@csrf_exempt
@require_POST
def nonvipuser(request):
    message = {}
    now = datetime.datetime.now()
    email = request.POST.get('email','')
    logger.info("email:%s",email)
    if email:
        try:
            access_vip = AccessVIPUser.objects.filter(expire__gt=now).select_related().get(email=email)
            access_user_list =[]
            if access_vip:
                message['is_print']= access_vip.is_print #为打印共享用户
                message['is_shared']= access_vip.is_shared #为文件共享用户
                message['remainder_print_num']= (access_vip.print_num - access_vip.used_print_num)
                message['remainder_shared_num']= (access_vip.shared_num - access_vip.used_shared_num)
                access_obj_set = access_vip.access_user_email.all()
                if access_obj_set:
                    for i in access_obj_set:
                        access_user_list.append(i.access_user_id)
                message['access_user']=access_user_list
                return HttpResponse(json.dumps(message),content_type="application/json")
        except Exception as e:
            logger.debug("access_vip:%s",e)
            try:
                access_user_set = AccessVIPUser.objects.filter(access_user_email__access_user=email).filter(expire__gt=now)
                if access_user_set:
                    is_print =False
                    is_shared =False
                    print_num =0
                    used_print_num = 0
                    shared_num = 0
                    used_shared_num = 0
                    for aus in access_user_set:
                        if aus.is_print:
                            is_print = True
                            print_num = aus.print_num
                            use_print_num = aus.used_print_num
                        if aus.is_shared:
                            is_shared =True
                            shared_num = aus.shared_num
                            used_shared_num = aus.used_shared_num
                    message['is_print']= is_print #为打印共享用户
                    message['is_shared']= is_shared #为文件共享用户
                    message['remainder_print_num']= (print_num - used_print_num)
                    message['remainder_shared_num']= (shared_num - used_shared_num)
                    message['access_user']=''
                    if settings.DEBUG:
                        pprint(message)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                else:
                    message['is_print']= False #为打印共享用户
                    message['is_shared']= False #为文件共享用户
                    message['remainder_print_num']= 0
                    message['remainder_shared_num']= 0
                    message['access_user']=''
                    return HttpResponse(json.dumps(message),content_type="application/json")
            except Exception as e:
                logger.debug("access_user:%s",e)
    else:
        message['message']='please post to me a email'
        message['status']="error"
        return HttpResponse(json.dumps(message),content_type="application/json")
