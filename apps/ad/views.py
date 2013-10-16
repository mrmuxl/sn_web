#_*_coding:utf-8_*_

import datetime,logging,json,os
from models import KxSoftAd,PrinterPop,FZu
from forms import PrinterPopForm
from apps.publish.models import KxPub
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_POST,require_GET)
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forms import OperatorForm
from apps.ad.models import Operator,OperatorAssistant,OperatorCategory
from apps.vipuser.views import get_remainder_days
from apps.kx.models import KxUserFriend


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
            data.update(ins_file=ins_file.install_file)
        except Exception as e:
            data.update(ins_file='')
            logger.debug("ins_file:%s",e)
        return render(request,"ad/print.html",data)
    if request.method == 'POST':
        data={"title":u"打印创业计划"}
        email = request.POST.get('pop','')
        if email:
            try:
                p = FZu.objects.create(email=email)
                p.save()
            except Exception as e:
                logger.debug("printer view:%s",e)
        try:
            ins_file = KxPub.objects.filter(pub_time__isnull=False).filter(install_file__istartswith='SimpleNect_V').order_by('-id')[0:1].get()
            data.update(ins_file=ins_file.install_file)
        except Exception as e:
            data.update(ins_file='')
            logger.debug("ins_file:%s",e)
        return render(request,"ad/print_result.html",data)

def fzu(request):
    if request.method == 'GET':
        data={"title":u"打印创业计划"}
        try:
            ins_file = KxPub.objects.filter(pub_time__isnull=False).filter(install_file__istartswith='SimpleNect_V').order_by('-id')[0:1].get()
            data.update(ins_file=ins_file.install_file)
        except Exception as e:
            data.update(ins_file='')
            logger.debug("ins_file:%s",e)
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
            data.update(ins_file=ins_file.install_file)
        except Exception as e:
            data.update(ins_file='')
            logger.debug("ins_file:%s",e)
        return render(request,"ad/print_result.html",data)

@login_required
def operator_add(request):
    if request.method == 'GET':
         #operator = operator.objects.get(user_id=request.user.pk)
        return render(request,"ad/operator_add_form.html",{})
    elif request.method == 'POST':
        form = OperatorForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user_id = request.user.pk
            f.save()
            try:
                data={"title":u"创业加盟"}
                ins_file = KxPub.objects.filter(pub_time__isnull=False).filter(install_file__istartswith='SimpleNect_V').order_by('-id')[0:1].get()
                data.update(ins_file=ins_file.install_file)
            except Exception as e:
                logger.debug("ins_file:%s",e)
            return render(request,"ad/print_result.html",data)
        return render(request,"ad/operator_add_form.html",{})
 
@csrf_exempt
@require_POST
def operator_select(request):
    '''运营专员接口'''
    message = {}
    now = datetime.datetime.now()
    email = request.POST.get('email','')
    logger.info("email:%s",email)
    remainder_days = get_remainder_days(email)
    if email:
        owner = Operator.objects.filter(status__exact=1).filter(expire__gt=now)
        opt = owner.filter(operatorassistant__user__email=email,operatorassistant__status__exact=1)
        if owner:
            message['status']=0
            message['is_owner']=True
            message['is_assistant']=False
            message['is_print']=True
            message['dislplay']=u'你可以共享一台打印机'
            message['printer_access']=u'http://www.simplenect.cn/User/printer/auth' #授权页面
            message['show_printer_access']=True
            message['buy_link']=u'http://www.simplenect.cn/buy'
            message['show_buy_link']=False
        if opt:
            message['status']=0
            message['is_owner']=False
            message['is_assistant']=True
            message['is_print']=True
            message['dislplay']=u'你可以共享一台打印机'
            message['buy_link']=u'http://www.simplenect.cn/buy'
            message['printer_access']=u'http://www.simplenect.cn/User/printer/auth' #授权页面
            message['show_printer_access']=False
            message['buy_link']=u'http://www.simplenect.cn/buy'
            message['show_buy_link']=False
            return HttpResponse(json.dumps(message,ensure_ascii=False),content_type="application/json")
        elif remainder_days <= 15:
            message['status']=0
            message['is_owner']=False
            message['is_assistant']=False
            message['is_print']=True
            message['dislplay']=u'你可以共享一台打印机,试用期还有'+ (15-remainder_days) + u'天'
            message['access']=u'http://www.simplenect.cn/User/printer/auth' #授权页面
            message['show_access']=False
            message['buy_link']=u'http://www.simplenect.cn/buy'
            message['show_buy_link']=True
            return HttpResponse(json.dumps(message,ensure_ascii=False),content_type="application/json")
        else:
            message['status']=0
            message['is_owner']=False
            message['is_assistant']=False
            message['is_print']=False
            message['dislplay']=u'您目前没有权限共享打印机'
            message['buy_link']=u'http://www.simplenect.cn/buy'#购买的链接这个用 buy_link比较合适
            message['printer_access']=u'http://www.simplenect.cn/User/printer/auth' #授权页面
            message['show_printer_access']=False#控制授权按钮显示
            message['show_buy_link']=True #控制 "购买" 按钮是否显示或许应该用 show_link
            return HttpResponse(json.dumps(message,ensure_ascii=False),content_type="application/json")
    else:
        message['status']=1
        return HttpResponse(json.dumps(message,ensure_ascii=False),content_type="application/json")

@csrf_exempt
@require_POST
def operator_show(request):
    message = {}
    now = datetime.datetime.now()
    email = request.POST.get('email','')
    logger.info("email:%s",email)
    friends=KxUserFriend.objects.filter(user=email).values('friend')
    operator_friends = Operator.objects.filter(user__email__in=friends).filter(status__exact=1).filter(expire__gt=now)
    c_id1 = []
    c_id2 = []
    c_id3 = []
    for i in operator_friends:
        if i.category.cid == 1:
            c_id1.append(i.user.email)
        if i.category.cid == 2:
            c_id2.append(i.user.email)
        if i.category.cid == 3:
            c_id3.append(i.user.email)
    of = [{"1":c_id1},{"2":c_id2},{"3":c_id3}]
    opt = Operator.objects.filter(user__email=email).filter(status__exact=1).filter(expire__gt=now).values('category__cid')
    if email:
        if opt:
            message['status']=0
            message['role']=opt[0]['category__cid']
            message['operator_friends']=of
            return HttpResponse(json.dumps(message),content_type="application/json")
        else :
            message['status']=0
            message['role']=4
            message['operator_friends']=of
            return HttpResponse(json.dumps(message),content_type="application/json")
    else:
        message['status']=1
        return HttpResponse(json.dumps(message),content_type="application/json")

