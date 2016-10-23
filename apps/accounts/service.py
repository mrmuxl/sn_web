#_*_coding:utf-8_*_

import datetime,logging,json,os
from apps.accounts.models import UserAuthIssue
logger = logging.getLogger(__name__)

def getUserAuthIssueByUser(uid):
	try:
		return UserAuthIssue.objects.get(user_id=uid)
	except Exception, e:
		logger.warn("获取用户验证问题失败！uid："+str(uid)+" %s",e)

def insertUserAuthIssue(userAuth):
	if isinstance(userAuth, UserAuthIssue):
		userAuth.save()
		return userAuth.id
	else:
		logger.error("the object's class must be UserAuthIssue")
		return None
def updateUserAuthIssueByCondition(condition,data):
		return UserAuthIssue.objects.filter(**condition).update(**data)