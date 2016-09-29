#_*_coding:utf-8_*_

import datetime,logging,json,os
from models import KxSoftAd,PrinterPop
from forms import PrinterPopForm
from apps.publish.models import KxPub
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

def printer(request):
    if request.method == 'GET':
        data={"title":u"打印创业计划"}
        try:
            ins_file = KxPub.objects.filter(pub_time__isnull=False).filter(install_file__istartswith='SimpleNect_V').order_by('-id')[0:1].get()
        except Exception as e:
            data.update(ins_file='')
            logger.debug("ins_file:%s",e)
        data.update(ins_file=ins_file.install_file)
        return render(request,"ad/print.html",data)
    if request.method == 'POST':
        data={"title":u"打印创业计划"}
        email = request.POST.get('pop','')
        if email:
            try:
                p = PrinterPop.objects.create(email=email)
                p.save()
            except Exception as e:
                logger.debug("printer view:%s",e)
        try:
            ins_file = KxPub.objects.filter(pub_time__isnull=False).filter(install_file__istartswith='SimpleNect_V').order_by('-id')[0:1].get()
        except Exception as e:
            data.update(ins_file='')
            logger.debug("ins_file:%s",e)
        data.update(ins_file=ins_file.install_file)
        return render(request,"ad/print_result.html",data)

def fzu(request):
    if request.method == 'GET':
        data={"title":u"打印创业计划"}
        try:
            ins_file = KxPub.objects.filter(pub_time__isnull=False).filter(install_file__istartswith='SimpleNect_V').order_by('-id')[0:1].get()
        except Exception as e:
            data.update(ins_file='')
            logger.debug("ins_file:%s",e)
        data.update(ins_file=ins_file.install_file)
        return render(request,"ad/fzu.html",data)
    if request.method == 'POST':
        data={"title":u"打印创业计划"}
        email = request.POST.get('pop','')
        if email:
            try:
                p = PrinterPop.objects.create(email=email)
                p.save()
            except Exception as e:
                logger.debug("printer view:%s",e)
        try:
            ins_file = KxPub.objects.filter(pub_time__isnull=False).filter(install_file__istartswith='SimpleNect_V').order_by('-id')[0:1].get()
        except Exception as e:
            data.update(ins_file='')
            logger.debug("ins_file:%s",e)
        data.update(ins_file=ins_file.install_file)
        return render(request,"ad/print_result.html",data)

