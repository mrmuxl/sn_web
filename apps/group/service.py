#_*_coding:utf-8_*_
import logging
from apps.group.models import *
logger = logging.getLogger(__name__)

def getGroupsListAll():
	"""获取群列表"""
	return Groups.objects.all().order_by("-create_time")

def getGroupsObjById(gid):
	"""根据ID获取群信息"""
	try:
		return Groups.objects.get(id=gid)
	except Exception,e:
		logger.warn("Groups not exists：gid="+str(gid)+" %s",e)
		return None

def getGroupsListByCondition(condition):
	"""根据condition获取群列表"""
	if isinstance(condition, dict):
		return Groups.objects.filter(**condition).order_by("-create_time")
	else:
		logger.error("the param of condition  must be the class dict")
		return None

def getGroupsCountByCondition(condition):
	"""根据condition获取群的数量"""
	if isinstance(condition, dict):
		return Groups.objects.filter(**condition).count()
	else:
		logger.error("the param of condition  must be the class dict")
		return None

def getPrintAuthListByCondition(condition):
	"""获取用户打印权限列表"""
	if isinstance(condition, dict):
		return PrintAuth.objects.filter(**condition)
	else:
		logger.error("the param of condition  must be the class dict")
		return None

def getUserPrinterObj(uid,code,mid):
	"""根据用户ID，打印据序列号code 机器码mid 获取单个用户打印机"""
	try:
		return UserPrinter.objects.get(print_user_id=uid,print_code=code,print_mid=mid)
	except Exception, e:
		logger.warn("UserPrint not exists：uid="+str(uid)+"  code="+str(code)+"  %s",e)
		return None

def getGroupUserObjByCondition(condition):
	if isinstance(condition, dict):
		try:
			return GroupUser.objects.get(**condition)
		except Exception,e:
			logger.warn("GroupUser not exists：condition="+str(condition)+"  %s",e)
			return None
	else:
		logger.error("the param of condition  must be the class dict")
		return None
def getGroupUserCountByCondition(condition):
	if isinstance(condition, dict):
		return GroupUser.objects.filter(**condition).count()
	else:
		logger.error("the param of condition  must be the class dict")
		return None

def getGroupUserListByCondition(condition):
	if isinstance(condition, dict):
		return GroupUser.objects.filter(**condition).order_by("-id")
	else:
		logger.error("the param of condition  must be the class dict")
		return None

def getGroupPrintCountByCondition(condition):
	"""根据condition获取打印机数量"""
	if isinstance(condition, dict):
		return GroupPrint.objects.filter(**condition).count()
	else:
		logger.error("the param of condition  must be the class dict")
		return None

def getPrintAuthObjByCondition(condition):
	"""根据condition群用户打印权限"""
	if isinstance(condition, dict):
		try:
			return PrintAuth.objects.get(**condition)
		except Exception,e:
			logger.warn("PrintAuth not exists：condition="+str(condition)+"  %s",e)
			return None
	else:
		logger.error("the param of condition  must be the class dict")
		return None

def getGroupUserInviteListByCondition(condition):
	"""根据condition群用户邀请列表"""
	if isinstance(condition, dict):
		return GroupUserInvite.objects.filter(**condition).order_by("-id")
	else:
		logger.error("the param of condition  must be the class dict")
		return None

def getGroupUserInviteObjByCondition(condition):
	if isinstance(condition, dict):
		try:
			return GroupUserInvite.objects.get(**condition)
		except Exception,e:
			logger.warn("GroupUserInvite not exists：condition="+str(condition)+"  %s",e)
			return None
	else:
		logger.error("the param of condition  must be the class dict")
		return None

def getGroupUserInviteCountByCondition(condition):
	if isinstance(condition, dict):
		return GroupUserInvite.objects.filter(**condition).count()
	else:
		logger.error("the param of condition  must be the class dict")
		return None

def insertUserPrinter(userPrinter):
	"""新增用户打印机"""
	if isinstance(userPrinter, UserPrinter):
		userPrinter.save()
		return userPrinter.id
	else:
		logger.error("the param's class must be UserPrinter")
		return None

def insertGroupPrint(groupPrint):
	"""新增群打印机"""
	if isinstance(groupPrint, GroupPrint):
		groupPrint.save()
		return groupPrint.id
	else:
		logger.error("the param's class must be GroupPrint")
		return None

def insertGroupUser(groupUser):
	"""新增群用户"""
	if isinstance(groupUser, GroupUser):
		groupUser.save()
		return groupUser.id
	else:
		logger.error("the param's class must be GroupUser")
		return None

def insertPrintAuth(printAuth):
	"""新增 群用户打印权限"""
	if isinstance(printAuth, PrintAuth):
		printAuth.save()
		return printAuth.id
	else:
		logger.error("the param's class must be PrintAuth")
		return None

def insertGroups(group):
	"""新增 群"""
	if isinstance(group, Groups):
		group.save()
		return group.id
	else:
		logger.error("the param's class must be Groups")
		return None

def updateUserPrinterByCondition(condition,data):
	"""更新打印机信息"""
	if isinstance(condition, dict) and isinstance(data,dict):
		return UserPrinter.objects.filter(**condition).update(**data)
	else:
		logger.error("the param of condition and data must be the class dict")
		return None
def updatePrintAuthByCondition(condition,data):
	"""更新群用户打印权限信息"""
	if isinstance(condition, dict) and isinstance(data,dict):
		return PrintAuth.objects.filter(**condition).update(**data)
	else:
		logger.error("the param of condition and data must be the class dict")
		return None

def updateGroupsByCondition(condition,data):
	"""更新群信息"""
	if isinstance(condition, dict) and isinstance(data,dict):
		return Groups.objects.filter(**condition).update(**data)
	else:
		logger.error("the param of condition and data must be the class dict")
		return None

def updateGroupUserByCondition(condition,data):
	"""更新群用户"""
	if isinstance(condition, dict) and isinstance(data,dict):
		return GroupUser.objects.filter(**condition).update(**data)
	else:
		logger.error("the param of condition and data must be the class dict")
		return None

def updateGroupPrintByCondition(condition,data):
	"""更新群打印机"""
	if isinstance(condition, dict) and isinstance(data,dict):
		return GroupPrint.objects.filter(**condition).update(**data)
	else:
		logger.error("the param of condition and data must be the class dict")
		return None

def updateGroupUserInviteByCondition(condition,data):
	"""更新邀请信息"""
	if isinstance(condition, dict) and isinstance(data,dict):
		return GroupUserInvite.objects.filter(**condition).update(**data)
	else:
		logger.error("the param of condition and data must be the class dict")
		return None

def delGroupPrintByCondition(condition):
	if isinstance(condition, dict) :
		return GroupPrint.objects.filter(**condition).delete()
	else:
		logger.error("the param of condition must be the class dict")
		return None

def delGroupUserByCondition(condition):
	"""删除群用户"""
	if isinstance(condition, dict) :
		return GroupUser.objects.filter(**condition).delete()
	else:
		logger.error("the param of condition must be the class dict")
		return None


def delGroupUserInviteByCondition(condition):
	"""删除群邀请用户"""
	if isinstance(condition, dict) :
		return GroupUserInvite.objects.filter(**condition).delete()
	else:
		logger.error("the param of condition must be the class dict")
		return None

def invitePipe(inviteList):
	"""在线用户的群邀请信息发送到消息管道"""
	""" 1001 表示群用户邀请;inviteList [{"uid":"dfe136","gid":10001,"gname":'abc',"create_time":'2013-05-06'}] """
	wfPath = "/home/admin/sn_web_fifo" #wfPath = "F:\sn_web\sn_web_fifo"
	wp = open(wfPath, 'a')
	msgList=[]
	for inv in inviteList:
		msg="1001#" + inv['uid'] + "," + inv['mac'] +"," + str(inv['gid']) + "," + inv['gname']+","+inv['create_time']+"\n"
		msgList.append(msg.encode("utf-8"))
		#msg= inv['gname'].encode("utf-8")
		logger.debug(msg)
	wp.writelines(msgList)
	wp.close()