#_*_coding:utf-8_*_

import datetime,logging,json
from models import VIPUser
from apps.kx.models import KxUserFriend
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_POST,require_GET)
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def vipuser_api(request):
    message = {}
    now = datetime.datetime.now()
    email = request.POST.get('email','')
    if email:
        friends=KxUserFriend.objects.filter(user=email).values('friend')
        vip_friends=VIPUser.objects.filter(is_vip__exact=1,email__in=friends).values('email')
        try:
            vipuser_obj = VIPUser.objects.get(email=email)
            if vipuser_obj.is_vip:
                message['is_vip']=True
                message['expire']=str(vipuser_obj.expire)
                message['status']="ok"
                return HttpResponse(json.dumps(message),content_type="application/json")
            elif vip_friends:
                message['is_vip']=False
                message['vip_friends']=list(vip_friends)
                message['status']="ok"
                return HttpResponse(json.dumps(message),content_type="application/json")
            else:
                message['is_vip']=False
                message['vip_friends']='no friends'
                message['status']="vip is overdue"
                return HttpResponse(json.dumps(message),content_type="application/json")
        except Exception as e:
            logger.debug("email not found:%s",e)
            message['is_vip']=False
            message['vip_friends']=list(vip_friends)
            message['status']="ok"
            return HttpResponse(json.dumps(message),content_type="application/json")
    else:
        message['message']='please post to me a email'
        message['status']="error"
        return HttpResponse(json.dumps(message),content_type="application/json")
