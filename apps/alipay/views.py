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

logger = logging.getLogger(__name__)

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
                        #vipuser = VIPUser.objects.filter(email=buy_user)
                        order_info.update(pay_status=1,pay_at=notify_time,trade_no=trade_no)
                        #这一段注释掉，订单只做订单处理，不和产品耦合,最初设计就是错误的，后来需求变更，导致这边代码成了累赘,vip用户准备用脚本异步做
                        #if vipuser:
                        #    myexpire = vipuser.values('expire')[0]['expire']
                        #    logger.info("expire:%s",myexpire)
                        #    if buy_product_id == 1:
                        #        if myexpire >= now:
                        #            try:
                        #                expire = myexpire + datetime.timedelta(days=365)
                        #                vipuser.update(is_vip=1,expire=expire)
                        #                logger.info("==>>VIPUser update email:%s,expire:%s",buy_user,expire)
                        #            except Exception as e:
                        #                logger.debug("==>>VIPUser update fail expire:%s,%s",expire,e)
                        #        else:
                        #            try:
                        #                expire = now + datetime.timedelta(days=365)
                        #                vipuser.update(is_vip=1,expire = expire)
                        #                logger.info("==>>VIPUser update email:%s,now:%s,expire:%s",buy_user,now,expire)
                        #            except Exception as e:
                        #                logger.debug("==>>VIPUser update fail:expire:%s",expire,e)
                        #    elif buy_product_id == 2:
                        #        if expire >= now:
                        #            try:
                        #                expire = myexpire + datetime.timedelta(days=182)
                        #                vipuser.update(is_vip=1,expire=expire)
                        #                logger.info("==>>VIPUser update email:%s,expire:%s",buy_user,expire)
                        #            except Exception as e:
                        #                logger.debug("==>>VIPUser update fail expire:%s,%s",expire,e)
                        #        else:
                        #            try:
                        #                expire = now + datetime.timedelta(days=365)
                        #                vipuser.update(is_vip=1,expire = expire)
                        #                logger.info("==>>VIPUser update email:%s,now:%s,expire:%s",buy_user,now,expire)
                        #            except Exception as e:
                        #                logger.debug("==>>VIPUser update fail:expire:%s",expire,e)
                        #else:
                        #    if buy_product_id == 1:
                        #        expire = now + datetime.timedelta(days=365)
                        #        VIPUser.objects.create(email=buy_user,is_vip=1,expire=expire)
                        #        logger.info("==>>VIPUser create product 1 email:%s,expire:%s",buy_user,expire)
                        #    else:
                        #        expire = now + datetime.timedelta(days=182)
                        #        VIPUser.objects.create(email=request.user,is_vip=1,expire=expire)
                        #        logger.info("==>>VIPUser create product 2 email:%s,expire:%s",buy_user,expire)
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

    try:
        uid = str(uuid.UUID.get_time_low(uuid.uuid1()))
        if len(uid) < 10:
            d = 10 - len(uid)
            for i in range(d):
                r = random.randint(0,9)
                uid = uid + str(r)
        order_id = time.strftime("%Y%m%d") + uid
        logger.info("order_id:%s",order_id)
        email = request.user.email
        logger.info("email:%s",email)
        number =1
        total_fee = number * price
        logger.info("buy_user:%s,order_id:%s,number:%s,total_fee:%s",email,order_id,number,total_fee)
        OrderInfo.objects.create(order_id=order_id,create_at=now,buy_user=email,buy_product_id=pid,number=number,total_fee=total_fee,pay_status=0,trade_no='0000')
    except Exception as e:
        logger.debug("order_result:%s",e)
    try:
        pay_url = create_direct_pay_by_user(order_id,name,desc,total_fee)
        logger.info("pay_url:%s",pay_url)
        return HttpResponse('ok')
        #return HttpResponseRedirect(pay_url)
    except Exception as e:
        logger.debug("pay_url_debug:%s",e)
        raise Http404
     

@login_required
@require_GET
def order_info(request):
    p = request.GET.get('c',u'1')
    #product_info = ProductInfo.objects.all()
    #p_list = []
    #for i in product_info:
    #    p_list.append(int(i.category))
    #if p and p is not None and p.isdigit():
    if p and  p.isdigit():
        if p == u'1':#VIP
            pdt_list = ProductInfo.objects.filter(category=p).filter(slug__isnull=False).order_by('order_num').values()
            return render(request,"alipay/order_info.html",{"pdt_list":pdt_list,"p":p})
        elif p == u'2': #打印机共享
            pdt_list = ProductInfo.objects.filter(category=p).filter(slug__isnull=False).order_by('order_num').values()
            return render(request,"alipay/print_share.html",{"pdt_list":pdt_list,"p":p})
        elif p == u'3': #打印机共享
            pdt_list = ProductInfo.objects.filter(category=p).filter(slug__isnull=False).order_by('order_num').values()
            return render(request,"alipay/file_share.html",{"pdt_list":pdt_list,"p":p})
        else:
            return HttpResponse(u'没有此类产品')
    else:
        return HttpResponse(u'参数错误')
