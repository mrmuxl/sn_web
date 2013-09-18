#_*_coding:utf-8_*_
import logging,json
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.kx.models import KxUser
from apps.online_user.models import OnlineUser
from apps.client.models import UserShortSerializer
from apps.client.decorators import sn_required
from django.http import HttpResponseRedirect,HttpResponse

logger = logging.getLogger(__name__)

#取好友的共享文件
@sn_required
@api_view(['GET'])
@authentication_classes((TokenAuthentication,SessionAuthentication))
@permission_classes((IsAuthenticated,))
def friendList(request):
	email = request.user.email     
	#email = 'falqs@foxmail.com'
	li = [] #OnlineUser.objects.raw('select o.lan_ip, o.wlan_ip, o.mac id, o.email from kx_userlogin o where o.email in (select friend from kx_user_friend where user=%s)  or o.email=%s', [email,email])
	for of in OnlineUser.objects.raw('select o.email, o.lan_ip, o.wlan_ip, o.mac  from kx_userlogin o where o.email in (select friend from kx_user_friend where user=%s)  or o.email=%s', [email,email]):
		li.append({"email":of.email, "lanIp":of.lan_ip, 'wlanIp':of.wlan_ip, 'appMac':of.mac})
	#li = OnlineUser.objects.all().values()


	friendList = []#KxUser.objects.raw('select u.id, u.email, u.nick, u.avatar, u.status, u.login_status from kx_user_friend f, kx_user u where f.user=%s and f.friend = u.email', [email])
	for friend in KxUser.objects.raw('select u.id, u.email, u.nick, u.avatar, u.status, u.login_status from kx_user_friend f, kx_user u where f.user=%s and f.friend = u.email', [email]):
		friendList.append({"email":friend.email, "nick":friend.nick, 'avatar':friend.avatar, 'status':friend.status, 'login_status':0})
	#	friend.login_status = 0
		# if(len(li) > 0):
		# 	for of in li:
		# 		if friend.email == of.email:
		# 			friend.login_status = 1
		# friendList.append(friend)


	#serializer = UserShortSerializer(friendList, many=True)

	#return Response(serializer.data)
	# print li
	# print friendList

	result = {}
	result['loginList'] = li
	result['friendList'] = friendList
	return Response(result)