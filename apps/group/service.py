#_*_coding:utf-8_*_
import logging
from apps.group.models import *
logger = logging.getLogger(__name__)

def getGroupPrintAuthListByCondition(condition):
	"""获取打印权限列表"""
	if isinstance(condition, dict):
		return GroupPrintAuth.objects.filter(**condition)
	else:
		logger.error("the param of condition  must be the class dict")
		return None

def getUserPrinterObj(uid,code):
	"""根据用户ID，打印据序列号code 获取单个用户打印机"""
	try:
		return UserPrinter.objects.get(print_user_id=uid,print_code=code)
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

def updateUserPrinterByCondition(condition,data):
	"""更新打印机信息"""
	if isinstance(condition, dict) and isinstance(data,dict):
		return UserPrinter.objects.filter(**condition).update(**data)
	else:
		logger.error("the param of condition and data must be the class dict")
		return None

def delGroupPrintByCondition(condition):
	if isinstance(condition, dict) :
		return GroupPrint.objects.filter(**condition).delete()
	else:
		logger.error("the param of condition must be the class dict")
		return None