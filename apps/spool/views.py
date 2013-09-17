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
        print origin_list,accept_list
        if origin_list:
            message['origin'] = str(origin_list)
        else:
            message['origin'] = []
        if accept_list:
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
            Spool.objects.filter(uuid=uuid).update(status=status,status_time=datetime.now())
            message['status'] = 0
            return HttpResponse(json.dumps(message),content_type="application/json")
        except Exception as e:
            message['status'] = 1
            return HttpResponse(json.dumps(message),content_type="application/json")
    else:
        message['status'] = 1
        return HttpResponse(json.dumps(message),content_type="application/json")


