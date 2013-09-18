#_*_coding:utf-8_*_

import logging,json,os
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_POST,require_GET)
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from forms import SpoolForm
from models import Spool 
from apps.kx.models import KxUserlogin
from django.conf import settings
from pprint import pprint
from datetime import datetime

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def spool_add(request):
    message = {}
    form = SpoolForm(request.POST)
    print request.POST
    if form.is_valid():
        form.save()
        message['status']=0
        return HttpResponse(json.dumps(message),content_type="application/json")
    else:
        message['status']=1
        return HttpResponse(json.dumps(message),content_type="application/json")

@csrf_exempt
@require_POST
def spool_select(request):
    message = {}
    email = request.POST.get('email','')
    mac  = request.POST.get('mac','')
    if email and mac:
        origin_list = Spool.objects.filter(origin_email=email).filter(origin_uuid=mac).order_by('print_time').values()
        accept_list = Spool.objects.filter(accept_email=email).filter(accept_uuid=mac).order_by('print_time').values()
        if origin_list:
            for i in origin_list:
                print_time = datetime.strftime(i['print_time'],"%Y-%m-%d %H:%M:%S")
                create_at = datetime.strftime(i['create_at'],"%Y-%m-%d %H:%M:%S")
                status_time = datetime.strftime(i['status_time'],"%Y-%m-%d %H:%M:%S")
                i['print_time'] = print_time
                i['create_at'] = create_at
                i['status_time'] = status_time
                print type(i['printer_name'])
                printer_name = i['printer_name'].decode().encode('gbk')
                printer_uuid = i['printer_uuid'].decode().encode('gbk')
                file_name = i['file_name'].decode().encode('gbk')
                file_path = i['file_path'].decode().encode('gbk')
                i['printer_name'] = printer_name
                i['printer_uuid'] = printer_uuid
                i['file_name'] = file_name
                i['file_path'] = file_path
            message['origin'] = list(origin_list)
        else:
            message['origin'] = []
        if accept_list:
            for i in accept_list:
                print_time = datetime.strftime(i['print_time'],"%Y-%m-%d %H:%M:%S")
                create_at = datetime.strftime(i['create_at'],"%Y-%m-%d %H:%M:%S")
                status_time = datetime.strftime(i['status_time'],"%Y-%m-%d %H:%M:%S")
                i['print_time'] = print_time
                i['create_at'] = create_at
                i['status_time'] = status_time
                printer_name = i['printer_name'].decode().encode('gbk')
                printer_uuid = i['printer_uuid'].decode().encode('gbk')
                file_name = i['file_name'].decode().encode('gbk')
                file_path = i['file_path'].decode().encode('gbk')
                i['printer_name'] = printer_name
                i['printer_uuid'] = printer_uuid
                i['file_name'] = file_name
                i['file_path'] = file_path
            message['accept'] = list(accept_list)
        else:
            message['accept'] = []
        message['status']= 0
        return HttpResponse(json.dumps(message),content_type="application/json")
    else:
        message['status']= 1
        return HttpResponse(json.dumps(message),content_type="application/json")

@csrf_exempt
@require_POST
def spool_update(request):
    message = {}
    uuid  = request.POST.get('uuid','')
    status = request.POST.get('status','')
    file_path = request.POST.get('file_path','')
    if uuid:
        try:
            spool_info = Spool.objects.filter(uuid=uuid)
            if file_path:
                spool_info.update(file_path=file_path,status_time=datetime.now())
            if status:
                spool_info.update(status=status,status_time=datetime.now())
                try:
                    sp_list = spool_info.values('origin_email','origin_uuid')
                    if sp_list:
                        user_online = KxUserlogin.objects.filter(email=sp_list[0]['origin_email']).filter(mac__contains=sp_list[0]['origin_uuid']).values('email','mac')
                        print user_online
                        if user_online:
                            p = "/home/admin/sn_web_fifo"
                            with open(p,"w") as f:
                                p = "100#" + user_online[0]['mac'] + user_oneline[0]['email'] + "\n"
                                f.write(p)
                except Exception as e:
                    logger.debug("spool_update:%s",e)
            message['status'] = 0
            return HttpResponse(json.dumps(message),content_type="application/json")
        except Exception as e:
            message['status'] = 1
            return HttpResponse(json.dumps(message),content_type="application/json")
    else:
        message['status'] = 1
        return HttpResponse(json.dumps(message),content_type="application/json")
