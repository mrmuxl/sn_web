 #_*_coding:utf-8_*_
from online_user.models import OnlineUser, OnlineUserSerializer
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def onlineFriends(request):
    email = request.user.email 
    email = 'falqs@foxmail.com'
    friendList = OnlineUser.objects.raw('select o.email, o.lan_ip, o.wlan_ip, o.mac id from kx_userlogin o where o.email in (select friend from kx_user_friend where user=%s)  or o.email=%s', [email,email])
    serializer = OnlineUserSerializer(friendList, many=True)

    return Response(serializer.data)

    #return render(request, 'sharefile/friendFiles.html')


