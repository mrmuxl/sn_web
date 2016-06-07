#_*_coding:utf-8_*_

import datetime,logging,json,os
from models import KxSoftAd
from django.views.decorators.http import (require_POST,require_GET)
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)

@require_GET
def ad_list(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('login'))
    else:
        try:
            ad_list = KxSoftAd.objects.order_by('-id').values()
            logger.info("%s",ad_list)
        except Exception as e:
            ad_list = []
            logger.debug("%s",e)
        t_var = {
                    'ad_list':ad_list,
                }
        return render(request,"ad/ad_list.html",t_var)
 
@require_GET
def ad_api(request):
    message = {}
    ad_dict = {}
    now = datetime.datetime.now()
    ad_list =list(KxSoftAd.objects.extra(where=['DATE(exp_day)>=CURDATE()']).order_by('-id').values('id','title','ad_url'))
    for i in ad_list:
        i.update(adUrl=i.pop('ad_url'))
    if ad_list:
        message['data']=ad_list
        message['status']="1"
        message['desc']= 'ok'
        return HttpResponse(json.dumps(message),content_type="application/json")
    else:
        message['data']=""
        message['status']="0"
        message['desc']= 'error'
        return HttpResponse(json.dumps(message),content_type="application/json")
