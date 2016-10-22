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
	uid = request.GET.get("uid").strip()
	name = request.GET.get("rname").strip()
	gid=0
	json_data={"status":0,"info":"edit remark error"}
	try:
		gid = int(request.GET.get("gid"))
	except Exception as e:
		logger.error("群ID必须为数字：%s",e)		
	
	if uid!="" and name!="" and gid>0 :
		print "ok-------"
	try:
		guser=GroupUser.objects.values("id","user_remark").filter(user_id=uid,group_id=gid)
		print "&****8"
		print guser
		#if guser:
		#	result=GroupUser.objects.filter(user_id=uid).update(user_remark=name)
		#else :
		#	json_data['info']="the group user not exists"

	except Exception as e:
		print e
		logger.error("修改群用户备注失败！%s",e)

	return HttpResponse(json.dumps(json_data),content_type="application/json")

