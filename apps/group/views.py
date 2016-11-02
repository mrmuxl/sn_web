#_*_coding:utf-8_*_

import datetime,logging,json,os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_POST,require_GET)
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Max
from apps.group.models import *
from apps.utils.json_util import *
from apps.utils.db_util import *
from apps.group.service import *
from apps.accounts.service import getUserCountByCondition,getUserObjByCondition

logger = logging.getLogger(__name__)

@csrf_exempt
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

@csrf_exempt
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
	sql="select g.id,g.printer_id,g.p_type,p.print_name,p.print_user_id,p.print_code,p.print_mid,p.remark,p.c_type from group_print g"\
		" left join user_printer p on g.printer_id=p.id where g.group_id=%s"	
	
	printList=query_sql(sql,[gid])
	authList=getPrintAuthListByCondition({"user_id":uid})
	authMap={} #用户的群打印机权限 组装成一个Map（dict)
	
	for auth in authList:
		authMap[auth.print_user_id]=auth.status

	# 群打印机的共享用户	
	puids=""
	for pt in printList:
		puids+=",'"+pt['print_user_id']+"'"
	issueMap={} #共享打印机的用户的验证提问
	issueList=[]
	if puids != "":
		puids=puids[1:]
		issueList=query_sql("select user_id,is_auth,issue from user_auth_issue where user_id in ("+puids+")")
     	for se in issueList :
     		issueMap[se['user_id']]=[]
     	 	issueMap[se['user_id']].append(se['is_auth'])
     		issueMap[se['user_id']].append(se['issue'])	
	
	json_data['status']=1
	json_data['info']="ok"
	json_data['print_list']=[]
	for pt in printList:
		puid=pt['print_user_id']
		status=-1 #用户未提交审核申请
		if puid in authMap.keys():
			status=authMap[puid]
		auth_type=0   #默认不需要验证
		issue=""
		if puid in issueMap.keys():
			auth_type=issueMap[puid][0]
			issue=issueMap[puid][1]

		json_data['print_list'].append({"puid":puid,"name":pt['print_name'],
					"code":pt['print_code'],"mid":pt['print_mid'],"remark":pt['remark'],"color":pt['c_type'],
					"type":pt['p_type'],"auth":status,"auth_type":auth_type,"issue":issue})

	return json_return(json_data,False)	

@csrf_exempt
@require_POST
def save_print(request):
	"""接口：添加群/编辑打印机 gid不传递表示修改打印机信息"""
	uid=request.POST.get("uid","").strip()
	name=request.POST.get("name","").strip()
	code=request.POST.get("code","").strip()
	mid=request.POST.get("mid","").strip()
	remark=request.POST.get("remark","").strip()
	flag=request.POST.get("flag","").strip()
	json_data={}
	json_data['status']=0
	gid=0
	pType=0
	cType=-1
	try:
		gid=int(request.POST.get("gid","0"))
		pType=int(request.POST.get("type","0"))
		cType=int(request.POST.get("color","-1"))
	except Exception,e:
		logger.error("群ID、打印机类型和色彩类型必须为数字：%s",e)
		json_data['info']="param err01"
		return json_return(json_data)
	if uid=="" or name=="" or code=="" or mid=="":
		json_data['info']="param err02"
		return json_return(json_data)
	#添加群打印机 或编辑打印机的类型
	if flag=="1":
		if gid<=0 or pType<=0 or pType>10 or cType<0 or cType>10:
			json_data['info']="param err03"
			return json_return(json_data)
		json_data=add_group_print(json_data,gid,uid,name,code,mid,remark,pType,cType)
	elif flag=="2" : 
		#修改群打印机名称备注等
		if cType<0 or cType>10:
			json_data['info']="param err04"
			return json_return(json_data)
		json_data=edit_group_print(json_data,uid,name,code,mid,remark,cType,pType,gid)	
	else :
		json_data['info']="param err05"
	return json_return(json_data)	


def add_group_print(json_data,gid,uid,name,code,mid,remark,pType,cType):
	guser=getGroupUserObjByCondition({"group_id":gid,"user_id":uid})
	if guser is None:
		json_data['info']="the group user not exists"
		return json_data
	if guser.share_print!=1:
		json_data['info']="the user can not share printer"
		return json_data

	userPrint=getUserPrinterObj(uid,code,mid)
	if userPrint is None:
		#用户打印机未上传过
		printerId=insertUserPrinter(UserPrinter(print_user_id=uid,print_name=name,print_code=code,print_mid=mid,remark=remark,c_type=cType))
		if not printerId>0:
			json_data['info']="add group printer err01"
			return json_data
		result=insertGroupPrint(GroupPrint(group_id=gid,printer_id=printerId,p_type=pType))
		if not result>0:
			json_data['info']="add group printer err02"
			return json_data
		json_data['status']=1
		json_data['info']="ok"
	else:
		#用户打印机已上传过
		printerId=userPrint.id
		gPrintNum=getGroupPrintCountByCondition({"printer_id":printerId,"group_id":gid})
		if gPrintNum is None:
			json_data['info']="add group printer err03"
		elif gPrintNum>0:
			json_data['status']=1
			json_data['info']="ok the group printer already exists "
		else:
			result=insertGroupPrint(GroupPrint(group_id=gid,printer_id=printerId,p_type=pType))
			if not result>0:
				json_data['info']="add group printer err04"
				return json_data
			else:
				json_data['status']=1
				json_data['info']="ok"
	return json_data


def edit_group_print(json_data,uid,name,code,mid,remark,cType,pType,gid):
	userPrint=getUserPrinterObj(uid,code)
	if userPrint is None:
		json_data['info']="the user printer not exists"
	else:
		result=updateUserPrinterByCondition({"print_user_id":uid,"print_code":code,"print_mid":mid},
											{"print_name":name,"remark":remark,"c_type":cType})
		if not result>0:
			json_data['info']="update user printer err01"
			return json_data
		if gid>0 and pType>0 and pType<=10:
			userPrint=getUserPrinterObj(uid,code,mid)
			if userPrint is None:
				json_data['info']="update user printer err02"
				return json_data
			result=updateGroupPrintByCondition({"group_id":gid,"printer_id":userPrint.id},{"p_type":pType})
			if not result>0:
				json_data['info']="update user printer err03"
				return json_data
		json_data['info']="ok"
		json_data['status']=1
	return json_data

@csrf_exempt
@require_POST
def del_print(request):
	"""接口：删除群打印机"""
	uid=request.POST.get("uid","").strip()
	code=request.POST.get("code","").strip()
	mid=request.POST.get("mid","").strip()
	gid=0
	json_data={}
	json_data['status']=0
	try:
		gid=int(request.POST.get("gid",0))
	except Exception,e:
		logger.error("群ID必须为数字：%s",e)
		json_data['info']="param err01"
		return json_return(json_data)
	if uid=="" or code=="" or gid<=0 or mid=="":
		json_data['info']="param err02"
		return json_return(json_data)
	userPrint=getUserPrinterObj(uid,code,mid)
	if userPrint is None:
		json_data['info']="the user printer is not exists"
		return json_return(json_data)
	delGroupPrintByCondition({"group_id":gid,"printer_id":userPrint.id})
	json_data['status']=1
	json_data['info']="ok"
	return json_return(json_data)

@csrf_exempt
@require_POST
def add_user(request):
	"""接口:用户加群 (包括高校用户自动加群) 目前只支持高校，普通群不支持"""
	json_data={}
	json_data['status']=0
	uid=request.POST.get("uid","").strip()
	try:
		gid=int(request.POST.get("gid",0))
	except Exception,e:
		logger.error("群ID必须为数字：%s",e)
		json_data['info']="param err01"
		return json_return(json_data)
	if gid <= 10000:
		json_data['info']="param err02"
		json_return(json_data)

	group=getGroupsObjById(gid)
	if group is None:
		json_data['info']="the group is not exists"
		return json_return(json_data)
	if group.user_num>=group.max_num:
		json_data['info']="the group user limit is reached"
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
			return json_return(json_data)
		result=updateGroupsByCondition({"id":gid},{"user_num":(group.user_num+1)})
		if not result>0:
			json_data['info']="add group user err02"
			return json_return(json_data)
		json_data['status']=1
		json_data['info']="ok"
	else:
		json_data['info']="this group user are not allowed to add"

	return json_return(json_data)

@csrf_exempt
@require_POST
def go_auth(request):
	"""接口:用户提交打印机审核"""
	json_data={}
	json_data['status']=0
	uid=request.POST.get("uid","").strip()
	puid=request.POST.get("puid","").strip()
	answer=request.POST.get("answer","").strip()
	if uid=="" or puid=="" :
		json_data['info']="param err01"
		return json_return(json_data)
	if uid==puid:
		json_data['info']="self not need to auth"
		return json_return(json_data)
	num=getGroupUserCountByCondition({"user_id":puid,"share_print":1})
	if not num>0:
		json_data['info']="the printer is not exists or allowed to share"
		return json_return(json_data)
	userNum=getUserCountByCondition({"uuid":uid})
	if userNum==0:
		json_data['info']="the user is not exists"
		return json_return(json_data)
	gpObj=getPrintAuthObjByCondition({"print_user_id":puid,"user_id":uid})
	if not gpObj is None:
		#审核拒绝后 用户再次提交审核请求，更新审核状态为0
		if gpObj.status==2:
			result=updatePrintAuthByCondition({"print_user_id":puid,"user_id":uid},{"status":0})
			if result>0:
				json_data['status']=1
				json_data['info']="ok"
			else:
				json_data['info']="update auth error"
			return json_return(json_data)
		else:
			json_data['info']="the user is already submitted"
			return json_return(json_data)
	result=insertPrintAuth(PrintAuth(print_user_id=puid,user_id=uid,status=0,answer=answer))
	if result>0:
		json_data['status']=1
		json_data['info']="ok"
	else:
		json_data['info']="add auth error"
	return json_return(json_data)

@csrf_exempt
@require_POST
def my_auth(request):
	"""接口:用户获取审核状态"""
	json_data={}
	json_data['status']=0
	uid=request.POST.get("uid","").strip()
	if uid=="":
		json_data['info']="param err01"
		return json_return(json_data)
	gpList=getPrintAuthListByCondition({"user_id":uid})
	json_data['status']=1
	json_data['info']="ok"
	json_data['auth_list']=[]
	for gp in gpList:
		json_data['auth_list'].append({"puid":gp.print_user_id,"verify":gp.status})
	return json_return(json_data)


@csrf_exempt
@require_POST
def list_auth(request):
	"""接口:共享用户获取审核列表"""
	json_data={}
	json_data['status']=0
	puid=request.POST.get("puid","").strip()
	if puid=="":
		json_data['info']="param err01"
		return json_return(json_data)
	num=getGroupUserCountByCondition({"user_id":puid,"share_print":1})
	if not num>0:
		json_data['info']="this printer is not exists or allowed to share"
		return json_return(json_data)
	sql="select a.*,u.email,u.nick from print_auth a left join kx_user u on a.user_id=u.uuid where a.status=0 and"\
		" a.print_user_id=%s"
	gpList=query_sql(sql,[puid])
	json_data['status']=1
	json_data['info']="ok"
	json_data['auth_list']=[]
	for gp in gpList:
		json_data['auth_list'].append({"uid":gp['user_id'],"email":gp['email'],"nick":gp['nick'],"answer":gp['answer'],
									   "time":str(gp['create_time'])})
	return json_return(json_data,False)

@csrf_exempt
@require_POST
def deal_auth(request):
	"""接口：处理审核状态"""
	json_data={}
	json_data['status']=0
	uid=request.POST.get("uid","").strip()
	puid=request.POST.get("puid","").strip()
	try:
		status=int(request.POST.get("verify",-1))
	except Exception,e:
		logger.error("verify 必须为数字：%s",e)
		json_data['info']="param err01"
		return json_return(json_data)
	if uid=="" or puid=="" or status<0 or status>2:
		json_data['info']="param err02"
		return json_return(json_data)
	num=getGroupUserCountByCondition({"user_id":puid,"share_print":1})
	if not num>0:
		json_data['info']="this printer is not exists or allowed to share"
		return json_return(json_data)
	result=updatePrintAuthByCondition({"print_user_id":puid,"user_id":uid},
											{"status":status,"auth_time":datetime.now()})
	if not result>0:
		json_data['info']="update  print auth err01"
	else:
		json_data['info']="ok"
		json_data['status']=1
	return json_return(json_data)

@csrf_exempt
@require_POST
def print_verify(request):
	"""接口：验证用户是否可以打印"""
	json_data={}
	json_data['status']=0
	json_data['info']=""
	uid=request.POST.get("uid","").strip()
	puid=request.POST.get("puid","").strip()
	mid=request.POST.get("mid","").strip()
	code=request.POST.get("code","").strip()
	if uid=="" or puid=="" or mid=="" or code=="":
		json_data['info']="param err01"
		return json_return(json_data)
	#自己跟自己无需验证
	if uid==puid:
		json_data['status']=1
		json_data['info']='ok'
		json_data['type']=1 #直接打印
		return json_return(json_data)	
	sql="select group_id,printer_id,p_type from group_print where printer_id = (select id from user_printer where " \
		" print_user_id=%s and print_code=%s and print_mid=%s)  order by p_type"
	gpList=query_sql(sql,[puid,code,mid])
	gIds=[]
	for gp in gpList:
		gIds.append(gp['group_id'])
	if len(gIds)==0:
		json_data['info']="no group has the print"
		return json_return(json_data)
	#打印用户在是否在指定的群里
	guList=GroupUser.objects.filter(user_id=uid,group_id__in=gIds)
	if len(guList)==0:
		json_data['info']="no group has the print"
		return json_return(json_data)
	guMap={}
	#print guList
	for gu in guList:
		guMap[gu.group_id]=gu.user_id
	for gp in gpList:
		gid=gp['group_id']
		#print "=========="
		if gid in guMap.keys():
			json_data['status']=1
			json_data['info']='ok'
			json_data['type']=gp['p_type']
			return json_return(json_data)		
	return json_return(json_data)



@require_GET
@login_required
def group_list(request):
	if not request.user.is_superuser:
		return HttpResponseRedirect(reverse("login"))
	groupList=getGroupsListAll()
	perNum=50
   	page=1
   	try:
   		page=int(request.GET.get("page"))
   	except Exception:
   		page=1
   	uids=[]
   	for group in groupList[(page-1)*perNum:page*perNum]:
   		#uids+=",'"+gu.user_id+"'"
   		uids.append(group.owner_id)
   	userMap=getUserMapByIds(uids)
	return render(request,"group/group_list.html",{"groupList":groupList,"userMap":userMap})

@login_required
def group_add(request):
	if not request.user.is_superuser:
		return HttpResponseRedirect(reverse("login"))
	res={}
	if request.method=="POST":
		name=request.POST.get("group_name","").strip()
		ownerEmail=request.POST.get("owner_email","").strip()
		try:
			gType=int(request.POST.get("g_type",0))
		except Exception, e:
			gType=0
		try:
			maxNum=int(request.POST.get("max_num",0))
		except Exception, e:
			maxNum=0
		try:
			gid=int(request.POST.get("gid",0))
		except Exception, e:
			gid=0
		errorMsg={}
		if name=="":
			errorMsg['group_name']="请填写群名！"
		else:
			res['group_name']=name
		if gType<=0 or gType>2:
			errorMsg['g_type']="请选择群类型！"
		else:
			res['g_type']=gType
		if maxNum<=0:
			errorMsg['max_num']="请填写群用户上限数（大于0的整数）！"
		else:
			res['max_num']=maxNum
		ownerId=""
		if ownerEmail=="":
			errorMsg['owner_email']="请填写群主email！"
		else:
			owner=getUserObjByCondition({"email":ownerEmail})
			if owner is None:
				errorMsg['owner_email']="该群主邮箱不存在！"
			else:
				ownerId=owner.uuid
			res['owner_email']=ownerEmail

		if errorMsg:
			res['error']=errorMsg
			return render(request,"group/group_add.html",res)
		if gid>0:
			#编辑群
			result=updateGroupsByCondition({"id":gid},{"name":name,"owner_id":ownerId,"max_num":maxNum})
			if result>0:
				return HttpResponseRedirect(reverse("group_group_list"))
			else:
				res['tip_error']="编辑群失败！"
		else:
			group=Groups(name=name,owner_id=ownerId,max_num=maxNum,g_type=gType,creater_id=request.user.uuid)
			if gType==2:
				maxId=Groups.objects.filter(id__gte=10001).filter(id__lte=19999).aggregate(max_id=Max('id'))
				print maxId
				if maxId['max_id'] is None:
					group.id=10001
				else:
					group.id=maxId['max_id']+1
			gid=insertGroups(group)
			if not gid is None:
				return HttpResponseRedirect(reverse("group_group_list"))
			else:
				res['tip_error']="新增群失败！"
	else:
		gid=request.GET.get("gid")
		if not gid is None and gid.strip()!="":
			res=edit_group(request,gid,res)

	return render(request,"group/group_add.html",res)

def edit_group(request,gid,res):
	res['gid']=gid
	try:
		gid=int(gid)
	except Exception,e:
		# 去错误提示页面
		logger.error("invalid gid : %s",e)
		res['tip_error']="该群不存在或已删除！"	
	else:
		group=getGroupsObjById(gid)
		if group is None:
			res['tip_error']="该群不存在或已删除！"	
			# 去错误提示页面
		else:
			owner=getUserObjByCondition({"uuid":group.owner_id})
			if owner is None:
				res['owner_email']=""
			else:
				res['owner_email']=owner.email
			res['group_name']=group.name
			res['g_type']=group.g_type
			res['max_num']=group.max_num	
	return res	

@login_required
@require_GET
def group_user(request):
	res={}
	try:
		gid=int(request.GET.get("gid",0))
	except Exception,e:
		logger.error("invalid gid %s",e)
		gid=0
	if gid <=0:
		res['error']="请选择一个群！"
		return render(request,"group/group_user.html",res)
	group=getGroupsObjById(gid)
	if group is None:
		res['error']="您查看的群不存在！"
		return render(request,"group/group_user.html",res)
	if (not request.user.is_superuser) and (group.owner_id!=request.user.uuid):
		res['error']="您无法查看该群成员信息！"
		return render(request,"group/group_user.html",res)
	res['group']=group
   	guList=getGroupUserListByCondition({"group_id":gid})
   	perNum=50
   	page=1
   	try:
   		page=int(request.GET.get("page"))
   	except Exception,e:
   		page=1
   	uids=[]
   	for gu in guList[(page-1)*perNum:page*perNum]:
   		#uids+=",'"+gu.user_id+"'"
   		uids.append(gu.user_id)
   	res['userMap']=getUserMapByIds(uids)
	res['guList']=guList
	return render(request,"group/group_user.html",res)

def getUserMapByIds(uids):
	"""根据uids 列表获取用户信息map"""
	userMap={}
	if len(uids)>0:
		userList=KxUser.objects.filter(uuid__in=uids)
		for user in userList:
			userMap[user.uuid]={}
			userMap[user.uuid]['uuid']=user.uuid
			userMap[user.uuid]['nick']=user.nick
			userMap[user.uuid]['email']=user.email
			userMap[user.uuid]['avatar']=user.avatar
	return userMap

@require_POST
def guser_add(request):
	"""Ajax 增加群用户"""
	json_data={}
	json_data['status']=0
	json_data,group,user=valid_group_user(request,json_data)
	if user is None:
		return json_return(json_data)

	if group.user_num>=group.max_num:
		json_data['info']="添加群用户失败！群用户数已达上限！"
		return json_return(json_data)
	count=getGroupUserCountByCondition({"group_id":group.id,"user_id":user.uuid})
	if count>0:
		json_data['info']="该用户已加入群里！"
		return json_return(json_data)
	uremark=request.POST.get("remark","")
	guId=insertGroupUser(GroupUser(group_id=group.id,user_id=user.uuid,user_remark=uremark,joiner_id=request.user.uuid))
	if not guId>0:
		json_data['info']="添加群用户失败！"
		return json_return(json_data)
	
	result=updateGroupsByCondition({"id":group.id},{"user_num":(group.user_num+1)})
	if not result>0:
		json_data['info']="添加群用户失败！err02"
		return json_return(json_data)
		
	json_data['status']=1
	json_data['info']="ok"
	json_data['email']=user.email
	json_data['nick']=user.nick
	json_data['remark']=uremark

	return json_return(json_data)

def valid_group_user(request,json_data):
	#判断用户是否登录
	if not request.user.is_authenticated():
		json_data['info']="请先登录!"
		return json_data,None,None
	email=request.POST.get("email","").strip()
	if email=="":
		json_data['info']="请填写用户邮箱！"
		return json_data,None,None
	try:
		gid=int(request.POST.get("gid"))
	except Exception,e:
		gid=0
		logger.error("invalid gid  %s",e)
	if gid<=0:
		json_data['info']="无效的群"
		return json_data,None,None
	group=getGroupsObjById(gid)
	if group is None:
		json_data['info']="该群不存在或已删除！"
		return json_data,None,None
	if (not request.user.is_superuser) and (group.owner_id!=request.user.uuid):
		json_data['info']="您无权限管理群用户！"
		return json_data,None,None
	user=getUserObjByCondition({"email":email})
	if user is None:
		json_data['info']="该用户邮箱不存在！"
		return json_data,None,None
	return json_data,group,user

@require_POST
def print_share(request):
	"""Ajax 更改群用户打印权限"""
	json_data={}
	json_data['status']=0
	json_data,group,user=valid_group_user(request,json_data)
	if user is None:
		return json_return(json_data)
	gu=getGroupUserObjByCondition({"group_id":group.id,"user_id":user.uuid})
	if gu is None:
		json_data['info']="该群用户不存在！"
		return json_return(json_data)
	share_print=0
	if gu.share_print==0:
		share_print=1
	result=updateGroupUserByCondition({"group_id":group.id,"user_id":user.uuid},{"share_print":share_print})
	if result:
		if share_print==0:
			#取消共享权限时，删除对应群里的用户打印机
			sql="delete from group_print where group_id=%s and printer_id in (select id from user_printer where print_user_id=%s)"
			result=execute_sql(sql,[group.id,user.uuid])
		json_data['status']=1
		json_data['info']="ok"
	else:
		json_data['info']="更改共享打印机权限失败！"
	return json_return(json_data)

@require_POST
def guser_del(request):
	"""Ajax 删除群用户"""
	json_data={}
	json_data['status']=0
	json_data,group,user=valid_group_user(request,json_data)
	if user is None:
		return json_return(json_data)
	delGroupUserByCondition({"group_id":group.id,"user_id":user.uuid})
	result=updateGroupsByCondition({"id":group.id},{"user_num":(group.user_num-1)})
	if not result>0:
		json_data['info']="删除群用户失败！"
		return json_return(json_data)
	json_data['status']=1
	json_data['info']="ok"
	return json_return(json_data)

@require_POST
def guser_remark(request):
	"""Ajax 更改群用户备注"""
	json_data={}
	json_data['status']=0
	json_data,group,user=valid_group_user(request,json_data)
	if user is None:
		return json_return(json_data)
	uremark=request.POST.get("remark","")
	result=updateGroupUserByCondition({"group_id":group.id,"user_id":user.uuid},{"user_remark":uremark})
	if result:
		json_data['status']=1
		json_data['info']="ok"
	else:
		json_data['info']="更改群用户备注失败！"
	return json_return(json_data)