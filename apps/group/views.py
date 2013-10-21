#_*_coding:utf-8_*_

import datetime,logging,json,os
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_POST,require_GET)
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.group.models import *

logger = logging.getLogger(__name__)

def user_remark(request):
	return render(request,"group/ad_list.html",{})
