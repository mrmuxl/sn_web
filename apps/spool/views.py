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
from apps.kx.models import KxUserLogin
from django.conf import settings
from pprint import pprint
from datetime import datetime

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def spool_add(request):
    message = {}
    form = SpoolForm(request.POST)
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
        origin_list = Spool.objects.filter(origin_email=email).filter(origin_uuid=mac).values()
        accept_list = Spool.objects.filter(accept_email=email).filter(accept_uuid=mac).values()
        if origin_list:
            for i in origin_list:
                print_time = datetime.strftime(i['print_time'],"%Y-%m-%d %H:%m:%s")
                create_at = datetime.strftime(i['create_at'],"%Y-%m-%d %H:%m:%s")
                status_time = datetime.strftime(i['status_time'],"%Y-%m-%d %H:%m:%s")
                i['print_time'] = print_time
                i['create_at'] = create_at
                i['status_time'] = status_time
            message['origin'] = str(origin_list)
        else:
            message['origin'] = []
        if accept_list:
            for i in accept_list:
                print_time = datetime.strftime(i['print_time'],"%Y-%m-%d %H:%m:%s")
                create_at = datetime.strftime(i['create_at'],"%Y-%m-%d %H:%m:%s")
                status_time = datetime.strftime(i['status_time'],"%Y-%m-%d %H:%m:%s")
                i['print_time'] = print_time
                i['create_at'] = create_at
                i['status_time'] = status_time
            message['accept'] = str(accept_list)
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
    if uuid and status:
        try:
            spool_info = Spool.objects.filter(uuid=uuid)
            spool_info.update(status=status,status_time=datetime.now())
            try:
                sp_list = spool_info.values('origin_email','origin_uuid')
                if sp_list:
                    user_online = KxUserLogin.objects.filter(email=sp_list[0]['origin_email']).(mac__contains=sp_list[0]['origin_uuid']).values('email','mac')
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


