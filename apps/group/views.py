#_*_coding:utf-8_*_

import datetime,logging,json,os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_POST,require_GET)
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.group.models import *
from apps.utils.json_util import *

logger = logging.getLogger(__name__)

@require_POST
def user_remark(request):
	uid = request.POST.get("uid",'').strip()
	name = request.POST.get("rname",'').strip()
	gid=0
	json_data={"status":0,"info":"edit remark error"}
	try:
		gid = int(request.POST.get("gid",0))
	except Exception as e:
		logger.error("群ID必须为数字：%s",e)
		json_data['info']="param err01"
		return json_return(json_data)		
	
	if uid!="" and name!="" and gid>0 :
		try:
			guser=GroupUser.objects.only("id","user_remark").filter(group_id=gid,user_id=uid)[:1]
			if guser:
				result=GroupUser.objects.filter(group_id=gid,user_id=uid).update(user_remark=name)
				if result:
					json_data['status']=1
					json_data['info']="OK"
				else:
					json_data['info']="update error"
			else :
				json_data['info']="the group user not exists"
			return json_return(json_data)
		except Exception as e:
			logger.error("修改群用户备注失败！%s",e)
			json_data['info']="param err01"
			return json_return(json_data)		
	else:
		json_data['info']="param err02"
		return json_return(json_data)

def group_print(request):
	uid=request.GET.get("uid")
	gid=0
	json_data={}
	try:
		gid = int(request.GET.get("gid",0))
	except Exception,e:
		logger.error("群ID必须为数字：%s",e)
		json_data['info']="param err01"
		return json_return(json_data)
	## 获取群打印机列表及当前用户的打印机权限
	return json_return(json_data)	




