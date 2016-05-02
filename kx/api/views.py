#_*_coding:utf-8_*_
import logging,json,sys,datetime,time,uuid
from kx.utils import is_valid_email
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from kx.models import (KxUser,KxSoftRecord,KxLanTongji,KxPubRecord)
from kx.models import (KxSoftUtime,KxEmailInvate)
from django.utils.html import strip_tags
from hashlib import md5
from django.core.mail import send_mail,EmailMultiAlternatives

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
                            ut_obj = KxSoftUtime.objects.create(client_identifie=cid,tongji_day=day,utime=ut,create_time=now)
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
    客户端注册接口
    '''
    now = datetime.datetime.now()
    message = {}
    word = [u'simplenect',u'运营',u'管理',u'系统']
    try:
        if request.method == 'POST':
            email = request.POST.get('email','')
            nick = request.POST.get('nick','')
            password = request.POST.get('password','')
            if email and nick and password:
                email = strip_tags(email.strip().lower())
                nick = strip_tags(nick.strip())
                password = strip_tags(password.strip())
                if not email:
                    message['message']=u'请填写邮箱email!'
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                if not is_valid_email(email):
                    message['message']=u'email邮箱格式不正确!'
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                if not nick:
                    message['message']=u'nick is null请填写昵称!'
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                if len(nick)<4 and len(nick)>12:
                    message['message']=u'nickname昵称应为4-12个字符!'
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                if nick in word:
                    message['message']=u'你被gfw墙了,昵称包含非法字符!'
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                if not password:
                    message['message']=u'password请填写密码!'
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                count = KxUser.objects.filter(email=email).count()
                if count > 0:
                    message['message']=u'another邮箱已经被使用,请更改一个可用的邮箱!'
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                try:
                    uid=md5(email).hexdigest()
                    create_user=KxUser.objects.create_user(uuid=uid,email=email,nick=nick,password=password,status=0)
                    create_user.save()
                    user = authenticate(username=email,password=password)
                except Exception as e:
                    logger.debug("%s",e)
                    message['message']=u'register 注册失败!请再重试一次!'
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                if user is not None and user.status == 0:
                    time_str = str(time.time())
                    chk = md5(email + "," + time_str + ",qianmo20120601").hexdigest()
                    ver_data =emial + "," + time_str + "," + chk
                    url =settings.DOMAIN + reverse('activate',args=[urlsafe_b64encode(ver_data),])
                    msg = "尊敬的SimpleNect用户，" + email + "：<br />&nbsp;&nbsp;您好！ <br />&nbsp;&nbsp;请点击以下链接激活您的账号：<a href='" + url + "'>" +     url + "</a>"
                    subject = '请激活帐号完成注册!'
                    from_email = 'SimpleNect <noreply@simaplenect.cn>'
                    EmailMultiAlternative(subject,msg,from_email,[email])
                    mail = EmailMultiAlternatives(subject,msg,from_email,[email])
                    mail.content_subtype = "html"
                    mail.send(fail_silently=True)
                    return HttpResponseRedirect('/User/account_verify/?email='+email)
    except Exception as e:
        logger.debug("cadd:%s",e,exc_info=True)
        info = "cadd:%s" %(e)
        message['message']=info
        message['create_time']=str(now)
        return HttpResponse(json.dumps(message),content_type="application/json")

def invate(request):
    '''邀请接口'''
    message = {}
    info = "Data save success"
    now = datetime.datetime.now()
    if request.method =="POST":
        my_email = request.POST.get('my_email','')
        invate_email = request.POST.get('invate_email','')
        my_name = request.POST.get('my_name','')
        invate_name = request.POST.get('nvate_name','')
        group_id = request.POST.get('group_id','')
        group_name = request.POST.get('group_name','')
        if my_email and invate_email and my_name and invate_name and group_id and group_name:
            my_email = my_email.strip()
            invate_name = invate_name.strip()
            if is_valid_email(my_email) and is_valid_email(invate_email):
                message['message']="check email"
                message['status']="ok"
                message['create_time']=str(now)
                return HttpResponse(json.dumps(message),content_type="application/json")
            my_name = my_name.strip()
            invate_name = invate_name.strip()
            group_id = group_id.strip()
            if not (group_id == -1 or group_id > 0):
                message['message']="group id error"
                message['status']="errors"
                message['create_time']=str(now)
                return HttpResponse(json.dumps(message),content_type="application/json")
            group_id = group_id.strip()
            try:
                user = KxUser.objects.get(email=my_emal)
                if user.uuid and user.uuid > 0:
                    try:
                        invate_code = md5(uuid.uuid4()).hexdigest()
                        invate_obj = KxEmailInvate.objects.create(user_id=user.uuid,user_name=my_name,invate_email=invate_email,group_id=group_id,group_name=group_name,invate_code=invate_code,qianmo_dot=0,create_time=now,status=0)
                        status = 1
                        url = settings.DOMAIN + reverse('invate_code',args=[invate_code])
                        if group_id == -1:
                            msg = "尊敬的" + invate_name + "：<br />&nbsp;&nbsp;您好！ <br />&nbsp;&nbsp;" + my_name + " 邀请您成为TA的好友，赶快注册并使用阡陌软件吧！<a href='" + url + "'>" + url + "</a>" 
                        else:
                            msg = "尊敬的" + invate_name + "：<br />&nbsp;&nbsp;您好！ <br />&nbsp;&nbsp;" + my_name + " 邀请您加入“" + group_name + "”群，赶快注册并使用阡陌软件吧！<a href='" + url + "'>" + url + "</a>" 
                        subject = '请激活帐号完成注册!'
                        from_email = 'SimpleNect <noreply@simaplenect.cn>'
                        mail = EmailMultiAlternatives(subject,msg,from_email,[invate_email])
                        mail.content_subtype = "html"
                        mail.send(fail_silently=True)
                        message['message']="invate ok"
                        message['status']="ok"
                        message['create_time']=str(now)
                        return HttpResponse(json.dumps(message),content_type="application/json")
                    except Exception as e:
                        logger.debug("%s",e)
                        message['message']="invate error"
                        message['status']="errors"
                        message['create_time']=str(now)
                        return HttpResponse(json.dumps(message),content_type="application/json")

            except user.DoesNotExist:
                message['message']="user dos not exist!"
                message['status']="errors"
                message['create_time']=str(now)
                return HttpResponse(json.dumps(message),content_type="application/json")
