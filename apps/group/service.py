#_*_coding:utf-8_*_
import logging
from apps.group.models import *
logger = logging.getLogger(__name__)

def getGroupsListAll():
	return Groups.objects.all().order_by("-id")

def getGroupPrintAuthListByCondition(condition):
	"""获取用户打印权限列表"""
	if isinstance(condition, dict):
		return GroupPrintAuth.objects.filter(**condition)
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

def getGroupPrintCountByCondition(condition):
	"""根据condition获取打印机数量"""
	if isinstance(condition, dict):
		return GroupPrint.objects.filter(**condition).count()
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

def getGroupPrintAuthObjByCondition(condition):
	"""根据condition群用户打印权限"""
	if isinstance(condition, dict):
		try:
			return GroupPrintAuth.objects.get(**condition)
		except Exception,e:
			logger.warn("GroupPrintAuth not exists：condition="+str(condition)+"  %s",e)
			return None
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

def insertGroupPrintAuth(printAuth):
	"""新增 群用户打印权限"""
	if isinstance(printAuth, GroupPrintAuth):
		printAuth.save()
		return printAuth.id
	else:
		logger.error("the param's class must be GroupPrintAuth")
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
def updateGroupPrintAuthByCondition(condition,data):
	"""更新群用户打印权限信息"""
	if isinstance(condition, dict) and isinstance(data,dict):
		return GroupPrintAuth.objects.filter(**condition).update(**data)
	else:
		logger.error("the param of condition and data must be the class dict")
		return None
def delGroupPrintByCondition(condition):
	if isinstance(condition, dict) :
		return GroupPrint.objects.filter(**condition).delete()
	else:
		logger.error("the param of condition must be the class dict")
		return None