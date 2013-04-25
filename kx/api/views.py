#_*_coding:utf-8_*_
import logging,json,sys,datetime,time
from kx.utils import is_valid_email
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from kx.models import (KxUser,KxSoftRecord,KxLanTongji,KxPubRecord)
from kx.models import (KxSoftUtime)
from django.utils.html import strip_tags
from hashlib import md5

logger = logging.getLogger(__name__)

@csrf_exempt
def record(request):
    now = datetime.datetime.now()
    message = {}
    info = "Data save success"
    is_uninstall = 0
    try:
        if request.method == 'POST':
            ver = request.POST.get('ver',None)
            cid = request.POST.get('clientIdentifie',None)
            md5str = request.POST.get('md5str',None)
            logger.info("ver:%s,cid:%s,md5str:%s",ver,cid,md5str,exc_info=True)
            if ver is not None and cid is not None and md5str is not None:
                ver = ver.rstrip('\n')
                cid = cid.rstrip('\n')
                verify=md5(ver+cid+'123456').hexdigest()
                if verify == md5str:
                    try:
                        record_count = KxSoftRecord.objects.filter(client_identifie__exact=cid).extra(where=['DATE(login_time)<CURDATE()']).count()
                        logger.info("record_count:%s",record_count)
                        if record_count == 0:
                            is_new = 1
                        else:
                            is_new = 0
                        record_obj = KxSoftRecord.objects.create(version = ver,client_identifie=cid,login_time=now,is_uninstall=is_uninstall,is_new=is_new)
                        message['message']=info
                        message['create_time']=str(now)
                        return HttpResponse(json.dumps(message),content_type="application/json")
                    except Exception as e:
                        logger.debug("record_count%s",e)
                        info = "%s" %(e)
                        message['message']=info
                        message['create_time']=str(now)
                        return HttpResponse(json.dumps(message),content_type="application/json")
                else:
                    message['message']=u"校验码不匹配"
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
            else:
                message['ver']=ver
                message['clientIDentifie']=cid
                message['md5str']=md5str
                message['create_time']=str(now)
                return HttpResponse(json.dumps(message),content_type="application/json")
        else:
            message['message']=u"No GET! Please POST!"
            message['create_time']=str(now)
            return HttpResponse(json.dumps(message),content_type="application/json")
    except Exception as e:
        logger.debug("record:%s",e,exc_info=True)
        info = "%s" %(e)
        message['message']=info
        message['create_time']=str(now)
        return HttpResponse(json.dumps(message),content_type="application/json")


@csrf_exempt
def uninstall(request):
    now = datetime.datetime.now()
    message = {}
    info = "Data save success"
    try:
        if request.method == 'POST':
            ver = request.POST.get('ver',None)
            cid = request.POST.get('clientIdentifie',None)
            md5str = request.POST.get('md5str',None)
            logger.info("ver:%s,cid:%s,md5str:%s",ver,cid,md5str,exc_info=True)
            if ver is not None and cid is not None and md5str is not None:
                ver = ver.rstrip('\n')
                cid = cid.rstrip('\n')
                verify=md5(ver+cid+'123456').hexdigest()
                if verify == md5str:
                    try:
                        is_new = 0
                        is_uninstall = 1
                        record_obj = KxSoftRecord.objects.create(version = ver,client_identifie=cid,login_time=now,is_uninstall=is_uninstall,is_new=is_new)
                        message['message']=info
                        message['create_time']=str(now)
                        return HttpResponse(json.dumps(message),content_type="application/json")
                    except Exception as e:
                        logger.debug("record_count%s",e)
                        info = "%s" %(e)
                        message['message']=info
                        message['create_time']=str(now)
                        return HttpResponse(json.dumps(message),content_type="application/json")
                else:
                    message['message']=u"校验码不匹配"
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
            else:
                message['ver']=ver
                message['clientIDentifie']=cid
                message['md5str']=md5str
                message['create_time']=str(now)
                return HttpResponse(json.dumps(message),content_type="application/json")
        else:
            message['message']=u"No GET! Please POST!"
            message['create_time']=str(now)
            return HttpResponse(json.dumps(message),content_type="application/json")
    except Exception as e:
        logger.debug("record:%s",e,exc_info=True)
        info = "%s" %(e)
        message['message']=info
        message['create_time']=str(now)
        return HttpResponse(json.dumps(message),content_type="application/json")

@csrf_exempt
def lan_record(request):
    '''
    局域网数据统计,软件启动后提交数据
    '''
    now = datetime.datetime.now()
    lan = {} 
    message = {}
    info = "Data save success"
    try:
        if request.method == 'POST':
            pc = request.POST.get('pc',None)
            qm = request.POST.get('qm',None)
            if pc is not None and qm is not None:
                pc = int(pc)
                qm = int(qm)
                logger.info("pc:%d,qm:%d",pc,qm)
                if pc >0 and qm > 0:
                    ip = request.META.get('REMOTE_ADDR','')
                    tongji_day = datetime.date.today()
                    #ip = '118.77.168.132'
                    #tongji_day = '2013-04-12'
                    try:
                        lan_tj = KxLanTongji.objects.get(ip=ip,tongji_day=tongji_day)
                        if pc > lan_tj.pc_num:
                            lan['pc_num'] = pc
                        if qm > lan_tj.qm_num:
                            lan['qm_num'] = qm
                        if len(lan) > 0:
                            if lan.has_key('pc_num'):
                                pc_num = lan['pc_num']
                            else:
                                pc_num = pc 
                            if lan.has_key('qm_num'):
                                qm_num = lan['qm_num']
                            else:
                                qm_num = qm 
                            lan_id = lan_tj.id
                            logger.info("pc_num:%s,qm_num:%s",pc_num,qm_num)
                            try:
                                lan_tj = KxLanTongji.objects.filter(id__exact=lan_id).update(ip=ip,tongji_day=tongji_day,pc_num=pc_num,qm_num=qm_num)
                                message['message']=info
                                message['create_time']=str(now)
                                return HttpResponse(json.dumps(message),content_type="application/json")
                            except Exception as e:
                                logger.debug(u"插入数据库失败!%s",e)
                                info = "%s" %(e)
                                message['message']=info
                                message['create_time']=str(now)
                                return HttpResponse(json.dumps(message),content_type="application/json")
                        message['message']=info
                        message['create_time']=str(now)
                        return HttpResponse(json.dumps(message),content_type="application/json")
                    except KxLanTongji.DoesNotExist as e:
                        logger.debug("%s",e)
                        pc_num = pc
                        qm_num = qm
                        logger.info("%s:%s",pc_num,qm_num)
                        try:
                            lan_tj = KxLanTongji.objects.create(id=None,ip=ip,tongji_day=tongji_day,pc_num=pc_num,qm_num=qm_num)
                            message['message']=info
                            message['create_time']=str(now)
                            return HttpResponse(json.dumps(message),content_type="application/json")
                        except Exception as e:
                            logger.debug("%s",e)
                            info = "%s" %(e)
                            message['message']=info
                            message['create_time']=str(now)
                            return HttpResponse(json.dumps(message),content_type="application/json")
                else:
                   message['message']=u"参数错误!"
                   message['create_time']=str(now)
                   return HttpResponse(json.dumps(message),content_type="application/json")
            else:
                message['message']=u"参数错误!"
                message['create_time']=str(now)
                return HttpResponse(json.dumps(message),content_type="application/json")
        else:
            message['message']=u"No GET! Please POST!"
            message['create_time']=str(now)
            return HttpResponse(json.dumps(message),content_type="application/json")

    except Exception as e:
        logger.debug("record:%s",e,exc_info=True)
        info = "%s" %(e)
        message['message']=info
        message['create_time']=str(now)
        return HttpResponse(json.dumps(message),content_type="application/json")


@csrf_exempt
def pub_record(request):
    '''
    发布24小时内统计数据记录
    '''
    now = datetime.datetime.now()
    message = {}
    info = "Data save success"
    try:
        if request.method == 'POST':
            email = request.POST.get('email',None)
            pub_type = request.POST.get('type',None)
            num = request.POST.get('num',None)
            if email is not None and pub_type is not None and num is not None:
                email = strip_tags(email.strip().lower())
                obj = int(pub_type)
                num_int = int(num)
                if obj > 0 and num_int >0:
                    if obj > 5:
                        message['message']=u"type error!"
                        message['create_time']=str(now)
                        return HttpResponse(json.dumps(message),content_type="application/json")
                    count = KxUser.objects.filter(email=email).count()
                    if count == 0:
                        message['message']=u"User is not exists!"
                        message['create_time']=str(now)
                        return HttpResponse(json.dumps(message),content_type="application/json")
                    try:
                        pub_record = KxPubRecord.objects.create(id=None,email=email,tongji_time=now,obj=obj,obj_val=num_int)
                        message['message']=info
                        message['create_time']=str(now)
                        return HttpResponse(json.dumps(message),content_type="application/json")
                    except Exception as e:
                        logger.debug("pub_record:%s",e,exc_info=True)
                        info = "%s" %(e)
                        message['message']=info
                        message['create_time']=str(now)
                        return HttpResponse(json.dumps(message),content_type="application/json")
                else:
                    message['message']=u"I am zero!"
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
            else:
                message['message']=u"Some boys is a girl?"
                message['create_time']=str(now)
                return HttpResponse(json.dumps(message),content_type="application/json")
        else:
            message['message']=u"No GET! Please POST!"
            message['create_time']=str(now)
            return HttpResponse(json.dumps(message),content_type="application/json")
    except Exception as e:
        logger.debug("pub_record:%s",e,exc_info=True)
        info = "%s" %(e)
        message['message']=info
        message['create_time']=str(now)
        return HttpResponse(json.dumps(message),content_type="application/json")
 

@csrf_exempt
def utime(request):
    '''
    登陆时长
    '''
    now = datetime.datetime.now()
    message = {}
    info = "Data save success"
    try:
        if request.method == 'POST':
            cid = request.POST.get('clientIdentifie',None)
            day = request.POST.get('day',None)
            utime = request.POST.get('utime',None)
            if cid is not None and day is not None and utime is not None:
                day = strip_tags(day.strip())
                cid = strip_tags(cid.strip().upper())
                ut = strip_tags(utime.strip())
                logger.info("day:%s,ut:%s",day,ut)
                if ut >0 and day:
                    try:
                        su = KxSoftUtime.objects.get(client_identifie=cid,tongji_day=day)
                        ut_id = su.id
                        try:
                            su_obj = KxSoftUtime.objects.filter(id__exact=ut_id).update(utime=ut)
                            message['message']=info
                            message['create_time']=str(now)
                            return HttpResponse(json.dumps(message),content_type="application/json")
                        except Exception as e:
                            logger.debug("su_obj%s",e)
                            info = "%s" %(e)
                            message['message']=info
                            message['create_time']=str(now)
                            return HttpResponse(json.dumps(message),content_type="application/json")
                    except Exception as e:
                        try:
                            ut_obj = KxSoftUtime.objects.create(id=None,client_identifie=cid,tongji_day=day,utime=ut,create_time=now)
                            message['message']=info
                            message['create_time']=str(now)
                            return HttpResponse(json.dumps(message),content_type="application/json")
                        except Exception as e:
                            logger.debug("ut_obj%s",e)
                            info = "%s" %(e)
                            message['message']=info
                            message['create_time']=str(now)
                            return HttpResponse(json.dumps(message),content_type="application/json")
                        logger.debug("su:%s",e)
                        info = "su:%s" %(e)
                        message['message']=info
                        message['create_time']=str(now)
                        return HttpResponse(json.dumps(message),content_type="application/json")
                else:
                    message['message']=u"Type error!"
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
            else:
                message['message']=u"Type error!"
                message['create_time']=str(now)
                return HttpResponse(json.dumps(message),content_type="application/json")
        else:
            message['message']=u"No GET! Please POST!"
            message['create_time']=str(now)
            return HttpResponse(json.dumps(message),content_type="application/json")
    except Exception as e:
        logger.debug("utime:%s",e,exc_info=True)
        info = "utime%s" %(e)
        message['message']=info
        message['create_time']=str(now)
        return HttpResponse(json.dumps(message),content_type="application/json")

@csrf_exempt
def cadd(request):
    '''
    登陆时长
    '''
    now = datetime.datetime.now()
    message = {}
    word = [u'simplenect',u'运营',u'管理',u'系统']
    info = "Data save success"
    try:
        if request.method == 'POST':
            email = request.POST.get('email',None)
            nick = request.POST.get('nick',None)
            password = request.POST.get('password',None)
            if email is not None and nick is not None and password is not None:
                email = strip_tags(email.strip().lower())
                nick = strip_tags(nick.strip())
                password = strip_tags(password.strip())
                if not email:
                    message['message']=u'请填写邮箱!'
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                if not is_valid_email(email):
                    message['message']=u'email邮箱格式不正确!'
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                if not nick:
                    message['message']=u'nick请填写昵称!'
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                if len(nick)<4 and len(nick)>12:
                    message['message']=u'昵称应为4-12个字符!'
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                if nick in word:
                    message['message']=u'昵称包含非法字符!'
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                if not password:
                    message['message']=u'请填写密码!'
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                count = KxUser.objects.filter(email=email).count()
                if count > 0:
                    message['message']=u'邮箱已经被使用,请更改一个可用的邮箱!'
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                try:
                    uid=md5(email).hexdigest()
                    create_user=KxUser.objects.create_user(auto_id=None,id=uid,email=email,nick=nick,password=password,status=0)
                    create_user.save()
                except Exception as e:
                    logger.debug("%s",e)
                    time_str = time.time()
                    chk = md5(email + "," + time_str + ",qianmo20120601").hexdigest()
                    ver_data =emial + "," + time_str + "," + chk
                    url = ''
                    msg = """尊敬的SimpleNect用户，" . 
                    $email . "：<br />&nbsp;&nbsp;您好！ 
                    <br />&nbsp;&nbsp;请点击以下链接激活您的账号：
                    <a href='" . $url . "'>" . $url . "</a>"""
                    sendmail
                    try:
                        user_obj = KxUser.objects.filter(email=email).update(status=1)
                    except Exception as e:
                        logger.debug("%s",e)
                    

                    
                    



    except Exception as e:
        logger.debug("cadd:%s",e,exc_info=True)
        info = "cadd:%s" %(e)
        message['message']=info
        message['create_time']=str(now)
        return HttpResponse(json.dumps(message),content_type="application/json")

