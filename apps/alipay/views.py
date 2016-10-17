#_*_coding:utf-8_*_

import logging,uuid,time,datetime,random
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_POST,require_GET)
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from lib.alipay import create_direct_pay_by_user
from lib.alipay import notify_verify
from models import OrderInfo,ProductInfo
from django.http import Http404
from apps.vipuser.models import VIPUser
from decimal import Decimal
from apps.alipay.models import OrderInfo
from apps.ad.models import Operator

logger = logging.getLogger(__name__)

def get_order_id():
    uid = str(uuid.UUID.get_time_low(uuid.uuid1()))
    if len(uid) < 10:
        d = 10 - len(uid)
        for i in range(d):
            r = random.randint(0,9)
            uid = uid + str(r)
    order_id = time.strftime("%Y%m%d") + uid
    logger.info("order_id:%s",order_id)
    return order_id

@require_GET
def return_url_handler(request):
    now = datetime.datetime.now()
    out_trade_no = request.GET.get('out_trade_no','')
    trade_no = request.GET.get('trade_no','')
    trade_status = request.GET.get('trade_status','')
    notify_time = request.GET.get('notify_time',now)
    logger.info("out_trade_no:%s,trade_no:%s,trade_status:%s,notify_time:%s",out_trade_no,trade_no,trade_status,notify_time)
    if trade_status  in ('TRADE_FINISHED','TRADE_SUCCESS'):
        order_info = OrderInfo.objects.filter(order_id=out_trade_no)
        order_list = order_info.values('order_id','pay_status','pay_at','trade_no','buy_product_id','buy_user')
        logger.info("order_list%s",order_list)
        if order_list:
            order_id = order_list[0]['order_id']
            pay_status = order_list[0]['pay_status']
            pay_at = order_list[0]['pay_at']
            my_trade_no = order_list[0]['trade_no']
            buy_product_id = order_list[0]['buy_product_id']
            buy_user = order_list[0]['buy_user']
            #product_info = ProductInfo.objects.filter(id=buy_product_id) #为什么要写这个呢？当初想法是什么为什么要查询product_info表?
            logger.info("order_id:%s,pay_status:%s,pay_at:%s",order_id,pay_status,pay_at)
            logger.info("my_trade_no:%s,buy_product_id:%s,buy_user:%s",my_trade_no,buy_product_id,buy_user)
            if not pay_status and trade_no != my_trade_no:
                if out_trade_no == order_id:
                    try:
                        order_info.update(pay_status=1,pay_at=notify_time,trade_no=trade_no)
                        #这一段注释掉，订单只做订单处理，不和产品耦合,最初设计就是错误的，后来需求变更，导致这边代码成了累赘,vip用户准备用脚本异步做
                        logger.info("==>>update successful:out_trade_no:%s,trade_no%s",out_trade_no,trade_no)
                        return render(request,"alipay/return_url.html",{'order_id':order_id})
                    except Exception as e:
                        logger.debug("==>>update fail:out_trade_no:%s,%s",out_trade_no,e)
                        return HttpResponse('fail')
                else:
                    logger.info("out_trade_no:%s,order_id:%s",out_trade_no,order_id)
                    return HttpResponse('fail')
            else:
                logger.info("This order is checkout==>order_id:%s",order_id)
                return render(request,"alipay/return_url.html",{'order_id':order_id})
                #return HttpResponse('success')
        else:
            return HttpResponse(u'order not found')
    else:
        logger.info("trade_status:%s",trade_status)
        return HttpResponse('fail')

@csrf_exempt
@require_POST
def notify_url_handler(request):
    now = datetime.datetime.now()
    if notify_verify(request.POST):
        out_trade_no = request.POST.get('out_trade_no','')
        trade_no = request.POST.get('trade_no','')
        trade_status = request.POST.get('trade_status','')
        notify_time = request.POST.get('notify_time',now)
        logger.info("out_trade_no:%s,trade_no:%s,trade_status:%s,notify_time:%s",out_trade_no,trade_no,trade_status,notify_time)
        if trade_status  in ('TRADE_FINISHED','TRADE_SUCCESS'):
            order_info = OrderInfo.objects.filter(order_id=out_trade_no)
            order_list = order_info.values('order_id','pay_status','pay_at','trade_no','buy_product_id','buy_user')
            logger.info("order_list%s",order_list)
            order_id = order_list[0]['order_id']
            pay_status = order_list[0]['pay_status']
            pay_at = order_list[0]['pay_at']
            my_trade_no = order_list[0]['trade_no']
            buy_product_id = order_list[0]['buy_product_id']
            buy_user = order_list[0]['buy_user']
            logger.info("order_id:%s,pay_status:%s,pay_at:%s",order_id,pay_status,pay_at)
            logger.info("my_trade_no:%s,buy_product_id:%s,buy_user:%s",my_trade_no,buy_product_id,buy_user)
            if not pay_status and trade_no != my_trade_no:
                if out_trade_no == order_id:
                    try:
                        order_info.update(pay_status=1,pay_at=notify_time,trade_no=trade_no)
                        logger.info("==>>update successful:out_trade_no:%s,trade_no%s",out_trade_no,trade_no)
                        return HttpResponse('success')
                    except Exception as e:
                        logger.debug("==>>update fail:out_trade_no:%s,%s",out_trade_no,e)
                        return HttpResponse('fail')
                else:
                    logger.info("out_trade_no:%s,order_id:%s",out_trade_no,order_id)
                    return HttpResponse('fail')
            else:
                logger.info("This order is checkout==>order_id:%s",order_id)
                return HttpResponse('success')
        else:
            logger.info("trade_status:%s",trade_status)
            return HttpResponse('fail')
    else:
        logger.info("request error!")
        return HttpResponse('fail')

@require_POST
def create_order(request):
    '''
    #查询订单表获得付款时间,如果订单的创建时间大于购买产品过期，直接创建
    #查询operator表获得过期时间#  
    #如果无订单，直接创建,不需要查运营商表，
    '''
    now = datetime.datetime.now()
    product_info = ProductInfo.objects.all()
    t = request.POST.get('type','')
    num = request.POST.get('auth','')
    remain_money = request.POST.get('remain_money','0')
    print t,num,remain_money
    if t and t.isdigit() and num and num.isdigit():
        for i in product_info:
            if int(t)== int(i.id):
                pid = i.id
                name = i.name
                desc = i.desc
                price = i.price
            else:
                continue
        try:
            order_id = get_order_id()
            email = request.user.email
            logger.info("email:%s",email)
            number =1
            total_fee = number * price* Decimal(num) - Decimal(remain_money)
            logger.info("buy_user:%s,order_id:%s,number:%s,total_fee:%s,num:%s",email,order_id,number,total_fee,num)
            OrderInfo.objects.create(order_id=order_id,create_at=now,buy_user=email,buy_product_id=pid,number=number,total_fee=total_fee,pay_status=0,trade_no='0000',auth_user_num=num)
        except Exception as e:
            logger.debug("order_result:%s",e)
        try:
            pay_url = create_direct_pay_by_user(order_id,name,desc,total_fee)
            logger.info("pay_url:%s",pay_url)
            return HttpResponseRedirect(pay_url)
            #return HttpResponse('ok')
        except Exception as e:
            logger.debug("pay_url_debug:%s",e)
    else:
        return HttpResponse(u'创建订单失败，请重试!')

@login_required
@require_GET
def order_info(request):
    '''#查询订单表，显示给客户曾经购买过的服务，第一点
    #如果购买过的服务的过期时间早于现在时间，那么就不显示客户曾经购买过
    #如果购买的服务没有过期，查询还剩余天数，计算还剩多少钱,用户应付款额度减去剩下的钱数就是实际付款额度
    '''
    now = datetime.datetime.now()
    c = request.GET.get('c',u'1')
    t = request.GET.get('type','')
    order_info = OrderInfo.objects.filter(buy_user=request.user.email).filter(pay_status__exact=1).values('pay_at','buy_product_id__name','buy_product_id__price')[0:1]
    operator = Operator.objects.filter(user__email = request.user.email).values('expire')
    if order_info and operator:
        expire_time = operator[0]['expire']
        pay_time = order_info[0]['pay_at']
        if expire_time > now:
            remain_days = (expire_time - now).days
        else:
            remain_days = 0
        remain_money = remain_days*0.50
    else:
        order_info=[]
        remain_money = 0
    if t and t.isdigit() and t == u'12': #buy
        return render(request,"buy.html",{})
    if c and  c.isdigit():
        if c == u'1':#VIP
            pdt_list = ProductInfo.objects.filter(category=c).filter(slug__isnull=False).order_by('order_num').values()
            #return render(request,"alipay/printer.html",{"pdt_list":pdt_list,"remain_money":remain_money,"order_info":order_info})
            return render(request,"alipay/printer.html",{"pdt_list":pdt_list,"remain_money":remain_money,"order_info":order_info})
        else:
            return HttpResponse(u'没有此类产品')
    else:
        return HttpResponse(u'参数错误')

def access_user_buy(request):
    return HttpResponseRedirect(reverse('buy'))

