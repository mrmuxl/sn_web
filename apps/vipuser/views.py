#_*_coding:utf-8_*_

import datetime,logging,json
from django.conf import settings
from models import VIPUser,Print,Shared,PrintAccess,SharedAccess
from apps.kx.models import KxUserFriend
from apps.kx.models import KxUser
from models import Print,Shared
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_POST,require_GET)
from django.http import HttpResponseRedirect,HttpResponse
from apps.kx.utils import is_valid_email,send_mail_thread
from django.utils.html import strip_tags
from mail_text import vipuser_tip
from pprint import pprint
from utils import access_user_print,access_user_shared

logger = logging.getLogger(__name__)


def get_remainder_days(email):
    now = datetime.datetime.now()
    Dday = datetime.datetime(2013,8,20) #1944-06-06
    ctime = KxUser.objects.filter(email=email).values('create_time')
    if ctime:
        ctime = ctime[0]['create_time']
        if ctime >= Dday:
            remainder_days = (now - ctime).days
        else:
            remainder_days = (now - Dday).days
    else:
        remainder_days = (now - Dday).days
    return remainder_days


@csrf_exempt
@require_POST
def vipuser_api(request):
    message = {}
    now = datetime.datetime.now()
    email = request.POST.get('email','')
    logger.info("email:%s",email)
    if email:
        v = VIPUser.objects.filter(email=email,is_vip__exact=1,expire__gt=now)
        p = Print.objects.filter(email=email,is_print__exact=1,expire__gt=now)
        s = Shared.objects.filter(email=email,is_shared__exact=1,expire__gt=now)
        pa = PrintAccess.objects.filter(access_user=email,status__exact=1)
        sa = SharedAccess.objects.filter(access_user=email,status__exact=1)
        remainder_days = get_remainder_days(email)
        if v:
            message['status']=1 #为VIP用户
            message['is_vip']=True
            message['remainder_days']=-1 #不显示
            message['vip_friends']='vip'
            p = access_user_print(email)
            s = access_user_shared(email)
            message.update(p)
            message.update(s)
            if settings.DEBUG:
                pprint(message)
            return HttpResponse(json.dumps(message),content_type="application/json")
        elif p or s:
            message['status']=0 #不为VIP用户
            message['is_vip']=False
            message['remainder_days']=-1 #不显示
            message['vip_friends']='vip'
            p = access_user_print(email)
            s = access_user_shared(email)
            message.update(p)
            message.update(s)
            if settings.DEBUG:
                pprint(message)
            return HttpResponse(json.dumps(message),content_type="application/json")
        elif pa or sa:
            message['status']=0 #不为VIP用户
            message['is_vip']=False
            message['remainder_days']=-1 #不显示
            message['vip_friends']='vip'
            if pa:
                message['is_print']= True #为打印共享用户
            else:
                message['is_print']= False #不为打印共享用户
            if sa:
                message['is_shared']= True #为文件共享用户
            else:
                message['is_shared']= False #不为文件共享用户
            message['remainder_print_num']= -1
            message['remainder_shared_num']= -1
            message['print_access_user']=[]
            message['shared_access_user']=[]
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
            message['print_access_user']=[]
            message['shared_access_user']=[]
            if settings.DEBUG:
                pprint(message)
            return HttpResponse(json.dumps(message),content_type="application/json")
        else:
            message['status']=0 #无权限使用
            message['remainder_days']=0 #无剩余天数
            message['is_vip']= False
            message['vip_friends']='no friends'
            p = access_user_print(email)
            s = access_user_shared(email)
            message.update(p)
            message.update(s)
            if settings.DEBUG:
                pprint(message)
            return HttpResponse(json.dumps(message),content_type="application/json")
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
    '''这个接口已经不使用'''
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
 
@csrf_exempt
@require_POST
def access_user(request):
    message = {}
    now = datetime.datetime.now()
    email = request.POST.get('email','')
    tp = request.POST.get('type','')
    users = request.POST.getlist('users','')
    logger.info("email:%s,tp:%s,users:%s",email,tp,users)
    if email and tp:
        if tp == u'1':
            try:
                ins_print = Print.objects.get(email=email)
                PrintAccess.objects.filter(email=email).update(status=0)
                if users:
                    for u in users:
                        try:
                            if ins_print.used_print_num <= ins_print.print_num:
                                u_ins = KxUser.objects.get(email=u)
                                PrintAccess.objects.create(email=ins_print,access_user=u_ins,create_at=now,status=1)
                                ins_print.used_print_num =len(users)
                                ins_print.save()
                                message['status']=0
                                message['message']="ok"
                            else:
                                message['status']=3
                                message['message']="do nothing"
                        except Exception as e:
                            logger.debug("print_access_user:%s",e)
                            message['status']=1
                            message['message']=str(e)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                else:
                    ins_print.used_print_num =len(users)
                    ins_print.save()
                    message['status']=0
                    message['message']="ok"
                    return HttpResponse(json.dumps(message),content_type="application/json")
            except Exception as e:
                message['status']=1
                message['message']=str(e)
                return HttpResponse(json.dumps(message),content_type="application/json")
        elif tp == u'2':
            try:
                ins_shared = Shared.objects.get(email=email)
                SharedAccess.objects.filter(email=email).update(status=0)
                if users:
                    for u in users:
                        try:
                            if ins_shared.used_shared_num <= ins_shared.shared_num:
                                u_ins = KxUser.objects.get(email=u)
                                SharedAccess.objects.create(email=ins_shared,access_user=u_ins,create_at=now,status=1)
                                ins_shared.used_shared_num = len(users)
                                ins_shared.save()
                                message['status']=0
                                message['message']="ok"
                            else:
                                message['status']=3
                                message['message']="do nothing"
                        except Exception as e:
                            logger.debug("shared_access:%s",e)
                            message['status']=1
                            message['message']=str(e)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                else:
                    ins_shared.used_shared_num = len(users)
                    ins_shared.save()
                    message['status']=0
                    message['message']="ok"
                    return HttpResponse(json.dumps(message),content_type="application/json")
            except Exception as e:
                message['status']=1
                message['message']=str(e)
                return HttpResponse(json.dumps(message),content_type="application/json")
    else:
        message['status']=2
        message['message']="error parameters"
        return HttpResponse(json.dumps(message),content_type="application/json")

