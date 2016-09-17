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
    now = datetime.datetime.now()
    product_info = ProductInfo.objects.all()
    t = request.POST.get('type',None)
    num = request.POST.get('auth',None)
    print_num = request.POST.get('print',None)
    file_num = request.POST.get('file',None)
    if print_num or file_num:
        order_id = get_order_id()
        email = request.user.email
        logger.info("email:%s",email)
        if print_num:
            number = print_num
            pid = 13
            name =u'打印共享用户授权' 
            desc =u'打印共享用户授权' 
        else:
            number = 0
        if file_num:
            num = file_num
            pid = 13
            name = u'文件共享用户授权' 
            desc = u'文件共享用户授权' 
        else:
            num =0
        total_fee = Decimal(str(int(number)*5.00))+Decimal(str(int(num)*5.00))
        logger.info("buy_user:%s,order_id:%s,number:%s,total_fee:%s,num:%s",email,order_id,number,total_fee,num)
        OrderInfo.objects.create(order_id=order_id,create_at=now,buy_user=email,buy_product_id=pid,number=number,total_fee=total_fee,pay_status=0,trade_no='0000',auth_user_num=num)
    else:
        if t and  t is not None and t.isdigit():
            for i in product_info:
                if int(t)== int(i.id):
                    pid = i.id
                    name = i.name
                    desc = i.desc
                    price = i.price
                else:
                    continue
        else:
            return HttpResponse(u'创建失败，参数错误!')
        if num and num is not None and num.isdigit():
            money = Decimal(str(int(num)*5.00))
        else:
            money = Decimal("0.00")
            num = 0
        try:
            order_id = get_order_id()
            email = request.user.email
            logger.info("email:%s",email)
            number =1
            total_fee = number * price + money
            logger.info("buy_user:%s,order_id:%s,number:%s,total_fee:%s,num:%s",email,order_id,number,total_fee,num)
            OrderInfo.objects.create(order_id=order_id,create_at=now,buy_user=email,buy_product_id=pid,number=number,total_fee=total_fee,pay_status=0,trade_no='0000',auth_user_num=num)
        except Exception as e:
            logger.debug("order_result:%s",e)
    try:
        pay_url = create_direct_pay_by_user(order_id,name,desc,total_fee)
        logger.info("pay_url:%s",pay_url)
        #return HttpResponse('ok')
        return HttpResponseRedirect(pay_url)
    except Exception as e:
        logger.debug("pay_url_debug:%s",e)
        #raise Http404
     

@login_required
@require_GET
def order_info(request):
    c = request.GET.get('c',u'1')
    t = request.GET.get('type','')
    if t and t.isdigit() and t == u'12': #buy
        return render(request,"buy.html",{})
    if c and  c.isdigit():
        if c == u'1':#VIP
            pdt_list = ProductInfo.objects.filter(category=c).filter(slug__isnull=False).order_by('order_num').values()
            return render(request,"alipay/order_info.html",{"pdt_list":pdt_list})
        elif c == u'2': #打印机共享
            pdt_list = ProductInfo.objects.filter(category=c).filter(slug__isnull=False).order_by('order_num').values()
            return render(request,"alipay/print_share.html",{"pdt_list":pdt_list})
        elif c == u'4': #文件共享
            pdt_list = ProductInfo.objects.filter(category=c).filter(slug__isnull=False).order_by('order_num').values()
            return render(request,"alipay/file_share.html",{"pdt_list":pdt_list})
        else:
            return HttpResponse(u'没有此类产品')
    else:
        return HttpResponse(u'参数错误')

def access_user_buy(request):
    return render(request,"alipay/access_user_buy.html",{})

