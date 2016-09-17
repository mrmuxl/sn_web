#_*_coding:utf-8_*_

import datetime,logging,json,os
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_POST,require_GET)
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from forms import SpoolForm
from models import Spool 
from django.conf import settings
from utils import publish_message

logger = logging.getLogger(__name__)

@require_POST
def spool_add(request):
    message = {}
    form = SpoolForm(request.POST)
    if form.is_valid():
        form.save()
        message['status']="ok"
        return HttpResponse(json.dumps(message),content_type="application/json")
    else:
        message['status']="error"
        return HttpResponse(json.dumps(message),content_type="application/json")

@require_POST
def spool_select(request):
    email = request.POST.get('email','')
    uuid  = request.POST.get('uuid','')
    if email and uuid:
        message['status']="ok"
        return HttpResponse(json.dumps(message),content_type="application/json")
    else:
        message['status']="error"
        return HttpResponse(json.dumps(message),content_type="application/json")


    
@require_POST
def spool_update(request):
    uuid  = request.POST.get('uuid','')
    status = request.POST.get('status','')
    if uuid and status:
        message['status']="ok"
        return HttpResponse(json.dumps(message),content_type="application/json")
    else:
        message['status']="error"
        return HttpResponse(json.dumps(message),content_type="application/json")


