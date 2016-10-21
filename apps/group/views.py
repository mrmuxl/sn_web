#_*_coding:utf-8_*_

import datetime,logging,json,os
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_POST,require_GET)
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.group.models import *

logger = logging.getLogger(__name__)

@require_GET
def user_remark(request):
	uid = request.GET.get("uid")
	name = request.GET.get("rname")
	gid = request.GET.get("gid")

	return HttpResponse(json.dumps({"status":0,"info":""}),content_type="application/json")
