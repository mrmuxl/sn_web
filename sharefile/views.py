 #_*_coding:utf-8_*_
from sharefile.models import ShareFile, ShareFileSerializer
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import logging
from redis_cache import get_redis_connection
from django.http import HttpResponse
from django.conf import settings;
import redis

POOL = redis.ConnectionPool(host=settings.REDIS_IP, port = settings.REDIS_PORT,
        db=settings.REDIS_DB_ONLINE_USER)


logger = logging.getLogger(__name__)

#两表关联，取相关的共享目录，取目录信息
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def friendFiles(request):
    logger.debug(request.user.email)
    email = request.user.email 
    #email = 'falqs@foxmail.com'
    fileList = ShareFile.objects.raw('select s.id, share_name, comment_count, size, owner_email, owner_mac, u.nick from kx_share s, kx_share_follow f, kx_user u where s.owner_email=u.email and f.kx_share_id=s.id and  f.follower_email = %s and s.is_del=0', [email])
    serializer = ShareFileSerializer(fileList, many=True)

    return Response(serializer.data)

    #return render(request, 'sharefile/friendFiles.html')



#1 把自己的ip告诉服务器 2拿对方打洞的端口
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def peerPort(request):
    mac = request.POST['mac']
    if mac in [None, '']:
       return HttpResponse('')

    logger.debug('mac: ' + mac)
    con = redis.Redis(connection_poll=POOL) 
    sPtr = con.lindex(mac, 11)
    if sPtr in [None, '']:
       return HttpResponse('')

    ptr = int(sPtr)
    logger.debug('ptr:%d', ptr*2)
    result = con.lindex(mac, ptr*2)
    logger.debug('result:'+  result)
    if result:
        #sendMyInfoToServer(request, mac)
        return HttpResponse(result)
    else:
        return HttpResponse('')

#write message to fifo
import os
import cPickle
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def sendMyInfoToServer(request):
    mac = request.POST['mac']
    uuid = request.POST['uuid']
    psw = request.POST['psw']

    msg = "1#" + mac + "," + uuid + "," + psw 
    logger.debug(msg)

    wfPath = "/home/admin/sn_web_fifo"
    wp = open(wfPath, 'w')
    wp.write(msg)
    wp.close()

    return HttpResponse('')
