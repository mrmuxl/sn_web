#_*_coding:utf-8_*_

import datetime,logging,json
from models import VIPUser
from apps.kx.models import KxUserFriend
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_POST,require_GET)
from django.http import HttpResponseRedirect,HttpResponse
from apps.kx.utils import is_valid_email,send_mail_thread
from django.utils.html import strip_tags
from mail_text import vipuser_tip

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def vipuser_api(request):
    message = {}
    now = datetime.datetime.now()
    email = request.POST.get('email','')
    logger.info("email:%s",email)
    if email:
        friends=KxUserFriend.objects.filter(user=email).values('friend')
        vip_friends=VIPUser.objects.filter(is_vip__exact=1,expire__gt=now,email__in=friends).values('email')
        logger.info("friends:%s;vip_friends:%s" %(friends,vip_friends))
        try:
            vipuser_obj = VIPUser.objects.get(email=email)
            if vipuser_obj.is_vip:
                message['status']=1
                message['vip_friends']='not needed'
                return HttpResponse(json.dumps(message),content_type="application/json")
            elif vip_friends:
                message['status']=2
                message['vip_friends']=list(vip_friends)
                return HttpResponse(json.dumps(message),content_type="application/json")
            else:
                message['status']=0
                message['vip_friends']='no friends'
                return HttpResponse(json.dumps(message),content_type="application/json")
        except Exception as e:
            logger.debug("email not found:%s",e)
            if vip_friends:
                message['status']=2
                message['vip_friends']=list(vip_friends)
                return HttpResponse(json.dumps(message),content_type="application/json")
            else:
                message['status']=0
                message['vip_friends']='no in tables'
                return HttpResponse(json.dumps(message),content_type="application/json")
    else:
        message['message']='please post to me a email'
        message['status']="error"
        return HttpResponse(json.dumps(message),content_type="application/json")

@csrf_exempt
@require_GET
def vipuser_test(reqeust,ckey,email):
    key = '518279d14e20e'
    download_url =u'http://download.simplenect.cn/Install/SimpleNect_S3.3.6.2.zip' 
    from_email =u"SimpleNect"
    if ckey and email and key == ckey:
        email = strip_tags(email.strip().strip('/').lower())
        if not is_valid_email(email):
            message ="""邮箱格式不正确！<A HREF="javascript:history.back()">返 回</A>"""
        subject = u'SimpleNect文件仓库3.3.6.4版本发布！'
        msg = vipuser_tip(download_url)
        try:
            send_mail_thread(subject,msg,from_email,[email],html=msg)
            logger.info("email:%s",email)
        except Exception as e:
            logger.debug("%s",e)
        return HttpResponse(email+' is send ok')
    else:
        message = """Key Error or No email to send !<A HREF="javascript:history.back()">返 回</A>"""
        return HttpResponse(message)
