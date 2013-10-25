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
from apps.utils.db_util import *
from apps.group.service import *
from apps.accounts.service import getUserCountByCondition

logger = logging.getLogger(__name__)

@require_POST
def user_remark(request):
	"""接口：修改用户备注"""
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

@require_POST
def list_print(request):
	"""接口：群打印机列表"""
	uid=request.POST.get("uid","").strip()
	gid=0
	json_data={}
	json_data['status']=0
	try:
		gid = int(request.POST.get("gid",0))
	except Exception , e:
		logger.error("群ID必须为数字：%s",e)
		json_data['info']="param err01"
		return json_return(json_data)
	if uid=="" or gid<=0 :
		json_data['info']="param err02"
		return json_return(json_data)
	sql="select g.id,g.printer_id,p.print_name,p.print_user_id,p.print_code from group_print g"\
		" left join user_printer p on g.printer_id=p.id and g.group_id=%s"	
	
	printList=query_sql(sql,[gid])
	authList=getGroupPrintAuthListByCondition({"group_id":gid,"user_id":uid})
	authMap={} #用户的群打印机权限 组装成一个Map（dict)
	
	for auth in authList:
		authMap[auth.print_user_id]=auth.status

	# 群打印机的共享用户	
	puids=""
	for pt in printList:
		puids+=",\'"+pt['print_user_id']+"\'"
	issueMap={} #共享打印机的用户的验证提问
	if puids!="":
		puids=puids[1:]
    	issueList=query_sql("select user_id,is_auth,issue from user_auth_issue where user_id in ("+puids+")")
    	for se in issueList:
    		issueMap[se['user_id']]=[]
    		issueMap[se['user_id']].append(se['is_auth'])
    		issueMap[se['user_id']].append(se['issue'])
	print issueMap
	json_data['status']=1
	json_data['info']="ok"
	json_data['print_list']=[]
	for pt in printList:
		puid=pt['print_user_id']
		status=-1
		if puid in authMap.keys():
			status=authMap[puid]

		#用户未提交审核申请
		if status==-1:
			#默认不需要验证
			auth_type=0
			issue=""
			if puid in issueMap.keys():
				auth_type=issueMap[puid][0]
				issue=issueMap[puid][1]

			json_data['print_list'].append({"puid":puid,"name":pt['print_name'],
					"code":pt['print_code'],"auth":status,"auth_type":auth_type,"issue":issue})
		else:	
			json_data['print_list'].append({"puid":puid,"name":pt['print_name'],"code":pt['print_code'],"auth":status})
	return json_return(json_data)	

@require_POST
def save_print(request):
	"""接口：添加群/编辑打印机 gid不传递表示修改打印机信息"""
	uid=request.POST.get("uid","").strip()
	name=request.POST.get("name","").strip()
	code=request.POST.get("code","").strip()
	remark=request.POST.get("remark","").strip()
	json_data={}
	json_data['status']=0
	gid=0
	try:
		gid=int(request.POST.get("gid","0"))
	except Exception,e:
		json_data['info']="param err01"
		return json_return(json_data)
	if uid=="" or name=="" or code=="":
		json_data['info']="param err02"
		return json_return(json_data)
	#添加群打印机
	if gid>0:
		json_data=add_group_print(json_data,gid,uid,name,code,remark)
	else : 
		#修改群打印机名称备注等
		json_data=edit_group_print(json_data,uid,name,code,remark)	
	return json_return(json_data)	


def add_group_print(json_data,gid,uid,name,code,remark):
	guser=getGroupUserObjByCondition({"group_id":gid,"user_id":uid})
	if guser is None:
		json_data['info']="the group user not exists"
		return json_data
	if guser.share_print!=1:
		json_data['info']="the user can not share printer"
		return json_data

	userPrint=getUserPrinterObj(uid,code)
	if userPrint is None:
		#用户打印机未上传过
		printerId=insertUserPrinter(UserPrinter(print_user_id=uid,print_name=name,print_code=code,remark=remark))
		if not printerId>0:
			json_data['info']="add group printer err01"
			return json_data
		result=insertGroupPrint(GroupPrint(group_id=gid,printer_id=printerId))
		if not result>0:
			json_data['info']="add group printer err02"
			return json_data
		json_data['status']=1
		json_data['info']="ok"
	else:
		#用户打印机未上传过
		printerId=userPrint.id
		gPrintNum=getGroupPrintCountByCondition({"printer_id":printerId,"group_id":gid})
		if gPrintNum is None:
			json_data['info']="add group printer err03"
		elif gPrintNum>0:
			json_data['status']=1
			json_data['info']="ok the group printer already exists "
		else:
			result=insertGroupPrint(GroupPrint(group_id=gid,printer_id=printerId))
			if not result>0:
				json_data['info']="add group printer err04"
				return json_data
			else:
				json_data['status']=1
				json_data['info']="ok"
	return json_data


def edit_group_print(json_data,uid,name,code,remark):
	userPrint=getUserPrinterObj(uid,code)
	if userPrint is None:
		json_data['info']="the user printer not exists"
	else:
		result=updateUserPrinterByCondition({"print_user_id":uid,"print_code":code},{"print_name":name,"remark":remark})
		if not result>0:
			json_data['info']="update user printer err01"
		else:
			json_data['info']="ok"
			json_data['status']=1
	return json_data

@require_POST
def del_print(request):
	"""接口：删除群打印机"""
	uid=request.POST.get("uid","").strip()
	code=request.POST.get("code","").strip()
	gid=0
	json_data={}
	json_data['status']=0
	try:
		gid=int(request.POST.get("gid",0))
	except Exception,e:
		json_data['info']="param err01"
		return json_return(json_data)
	if uid=="" or code=="" or gid<=0:
		json_data['info']="param err02"
		return json_return(json_data)
	userPrint=getUserPrinterObj(uid,code)
	if userPrint is None:
		json_data['info']="the user printer is not exists"
		return json_return(json_data)
	delGroupPrintByCondition({"group_id":gid,"printer_id":userPrint.id})
	json_data['status']=1
	json_data['info']="ok"
	return json_return(json_data)

@require_POST
def add_user(request):
	"""接口:用户加群 (包括高校用户自动加群) 目前只支持高校，普通群不支持"""
	json_data={}
	json_data['status']=0
	uid=request.POST.get("uid","").strip()
	try:
		gid=int(request.POST.get("gid",0))
	except Exception,e:
		json_data['info']="param err01"
		return json_return(json_data)
	if gid <= 10000:
		json_data['info']="param err02"
		json_return(json_data)

	groupNum=getGroupsCountByCondition({"id":gid})
	if not groupNum>0:
		json_data['info']="the group is not exists"
		return json_return(json_data)

	userCount=getUserCountByCondition({"uuid":uid})
	if not userCount>0:
		json_data['info']="the user is not exists"
		return json_return(json_data)

	if gid>=10001 and gid<20000:
		userNum=getGroupUserCountByCondition({"group_id":gid,"user_id":uid})
		if userNum>0:
			json_data['info']="the group user is already exists"
			return json_return(json_data)
		result=insertGroupUser(GroupUser(group_id=gid,user_id=uid,share_print=0))
		if not result>0:
			json_data['info']="add group user err"
		else:
			json_data['status']=1
			json_data['info']="ok"
	else:
		json_data['info']="this group user are not allowed to add"

	return json_return(json_data)


def go_auth(request):
	"""接口:用户提交打印机审核"""
	json_data={}
	json_data['status']=0
	uid=request.POST.get("uid","").strip()
