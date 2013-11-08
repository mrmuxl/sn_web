#_*_coding:utf-8_*_

import logging,json,os
from apps.accounts.models import UserAuthIssue
from apps.kx.models import KxUser
logger = logging.getLogger(__name__)


def getUserCountByCondition(condition):
	if isinstance(condition, dict):
		return KxUser.objects.filter(**condition).count()
	else:
		logger.error("the param of condition  must be the class dict")
		return None

def getUserObjByCondition(condition):
	if isinstance(condition, dict):
		try:
			return KxUser.objects.get(**condition)
		except Exception,e:
			logger.warn("KxUser not exists：condition="+str(condition)+"  %s",e)
			return None
	else:
		logger.error("the param of condition  must be the class dict")
		return None

def getUserAuthIssueByUser(uid):
	try:
		return UserAuthIssue.objects.get(user_id=uid)
	except Exception, e:
		logger.warn("UserAuthIssue not exists uid："+str(uid)+" %s",e)
		return None

def insertUserAuthIssue(userAuth):
	if isinstance(userAuth, UserAuthIssue):
		userAuth.save()
		return userAuth.id
	else:
		logger.error("the param's class must be UserAuthIssue")
		return None
def updateUserAuthIssueByCondition(condition,data):
	if isinstance(condition, dict) and isinstance(data,dict):
		return UserAuthIssue.objects.filter(**condition).update(**data)
	else:
		logger.error("the param of condition and data must be the class dict")
		return None

def updateUserByCondition(condition,data):
	if isinstance(condition, dict) and isinstance(data,dict):
		return KxUser.objects.filter(**condition).update(**data)
	else:
		logger.error("the param of condition and data must be the class dict")
		return None