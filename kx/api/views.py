#_*_coding:utf-8_*_
import logging,json,sys,datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from kx.models import KxSoftRecord
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
    except Exception as e:
        logger.debug("record:%s",e,exc_info=True)
        info = "%s" %(e)
        message['message']=info
        message['create_time']=str(now)
        return HttpResponse(json.dumps(message),content_type="application/json")

@csrf_exempt
def lan_record(request):
    pc = request.POST.get('pc',None)
    qm = request.POST.get('qm',None)
    if pc is not None and qm is not None:
        pc = int(pc)
        qm = int(qm)
        if pc >0 and qm > 0:
            ip = request.META.get('REMOTE_ADDR','')
            tongji_day = datetime.date.today()



