#_*_coding:utf-8_*_
import logging,json,sys,datetime
from django.core.validators import email_re
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from kx.models import KxSoftRecord,KxLanTongji
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
            email = strip_tags(request.POST.get("email").strip())
            email = request.POST.get('email',None)
            pub_type = request.POST.get('type',None)
            num = request.POST.get('num',None)
            if email is not None and pub_type is not None and num is not None:
                type_int = int(pub_type)
                num_int = int(num)
                if type_int > 0 and num_int >0:
                    if type_int > 5:
                        message['message']=u"type error!"
                        message['create_time']=str(now)
                        return HttpResponse(json.dumps(message),content_type="application/json")
                    email = strip_tags(email.strip().lower())




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
