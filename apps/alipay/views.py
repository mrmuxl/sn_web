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

def notify_verify(p):
    return True

@require_GET
def return_url_handler(request):
    now = datetime.datetime.now()
    if notify_verify(request.GET):
        out_trade_no = request.GET.get('out_trade_no','')
        trade_no = request.GET.get('trade_no','')
        trade_status = request.GET.get('trade_status','')
        notify_time = request.GET.get('notify_time',now)
        logger.info("out_trade_no:%s,trade_no:%s,trade_status:%s,notify_time:%s",out_trade_no,trade_no,trade_status,notify_time)
        if trade_status  in ('TRADE_FINISHED','TRADE_SUCCESS'):
            order_info = OrderInfo.objects.filter(order_id=out_trade_no)
            print dir(order_info)
            order_list = order_info.values('order_id','pay_status','pay_at','trade_no','buy_product_id','buy_user')
            logger.info("order_list%s",order_list)
            order_id = order_list[0]['order_id']
            pay_status = order_list[0]['pay_status']
            pay_at = order_list[0]['pay_at']
            my_trade_no = order_list[0]['trade_no']
            buy_product_id = order_list[0]['buy_product_id']
            buy_user = order_list[0]['buy_user']
            product_info = ProductInfo.objects.filter(id=buy_product_id)
            print product_info.values()
            print dir(product_info)
            logger.info("order_id:%s,pay_status:%s,pay_at:%s",order_id,pay_status,pay_at)
            logger.info("my_trade_no:%s,buy_product_id:%s,buy_user:%s",my_trade_no,buy_product_id,buy_user)
            if not pay_status and trade_no != my_trade_no:
                if out_trade_no == order_id:
                    try:
                        vipuser = VIPUser.objects.filter(email=buy_user)
                        order_info.update(pay_status=1,pay_at=notify_time,trade_no=trade_no)
                        if vipuser:
                            myexpire = vipuser.values('expire')[0]['expire']
                            logger.info("expire:%s",myexpire)
                            if buy_product_id == 1:
                                if myexpire >= now:
                                    try:
                                        expire = myexpire + datetime.timedelta(days=365)
                                        vipuser.update(is_vip=1,expire=expire)
                                        logger.info("==>>VIPUser update email:%s,expire:%s",buy_user,expire)
                                    except Exception as e:
                                        logger.debug("==>>VIPUser update fail expire:%s,%s",expire,e)
                                else:
                                    try:
                                        expire = now + datetime.timedelta(days=365)
                                        vipuser.update(is_vip=1,expire = expire)
                                        logger.info("==>>VIPUser update email:%s,now:%s,expire:%s",buy_user,now,expire)
                                    except Exception as e:
                                        logger.debug("==>>VIPUser update fail:expire:%s",expire,e)
                            elif buy_product_id == 2:
                                if expire >= now:
                                    try:
                                        expire = myexpire + datetime.timedelta(days=182)
                                        vipuser.update(is_vip=1,expire=expire)
                                        logger.info("==>>VIPUser update email:%s,expire:%s",buy_user,expire)
                                    except Exception as e:
                                        logger.debug("==>>VIPUser update fail expire:%s,%s",expire,e)
                                else:
                                    try:
                                        expire = now + datetime.timedelta(days=365)
                                        vipuser.update(is_vip=1,expire = expire)
                                        logger.info("==>>VIPUser update email:%s,now:%s,expire:%s",buy_user,now,expire)
                                    except Exception as e:
                                        logger.debug("==>>VIPUser update fail:expire:%s",expire,e)
                        else:
                            if buy_product_id == 1:
                                expire = now + datetime.timedelta(days=365)
                                VIPUser.objects.create(email=buy_user,is_vip=1,expire=expire)
                                logger.info("==>>VIPUser create product 1 email:%s,expire:%s",buy_user,expire)
                            else:
                                expire = now + datetime.timedelta(days=182)
                                VIPUser.objects.create(email=request.user,is_vip=1,expire=expire)
                                logger.info("==>>VIPUser create product 2 email:%s,expire:%s",buy_user,expire)
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
                return HttpResponse('success')
        else:
            logger.info("trade_status:%s",trade_status)
            return HttpResponse('fail')
    else:
        logger.info("request error!")
        return HttpResponse('fail')

@csrf_exempt
@require_POST
def notify_url_handler(request):
    now = datetime.datetime.now()
    if notify_verify(request.POST):
        out_trade_no = request.POST.get('out_trade_no','')
        trade_no = request.GET.get('trade_no','')
        trade_status = request.GET.get('trade_status','')
        trade_status = request.POST.get('trade_status','')
        notify_time = request.POST.get('notify_time',now)
        logger.info("out_trade_no:%s,trade_no:%s,trade_status:%s,notify_time%s",out_trade_no,trade_no,trade_status,notify_time)
        if trade_status  in ('TRADE_FINISHED','TRADE_SUCCESS'):
            order_info = OrderInfo.objects.filter(order_id=out_trade_no)
            order_list = order_info.values('order_id','pay_status','pay_at','trade_no')
            order_id = order_list[0]['order_id']
            pay_status = order_list[0]['pay_status']
            pay_at = order_list[0]['pay_at']
            my_trade_no = order_list[0]['trade_no']
            logger.info("order_id:%s,pay_status:%s,pay_at:%s,my_trade_no",order_id,pay_status,pay_at,my_trade_no)
            if not pay_status and trade_no != my_trade_no:
                if out_trade_no == order_id:
                    try:
                        order_info.update(pay_status=1,pay_at=notify_time,trade_no=trade_no)
                        if buy_product_id == 1:
                            vipuser = VIPUser.objects.filter(email=buy_user)
                            if vipuser:
                                myexpire = vipuser.values('expire')[0]['expire']
                                logger.info("myexpire:%s",myexpire)
                                if myexpire >= now:
                                    vipuser.update(is_vip=1,expire=(myexpire + datetime.timedelta(days=365)))
                                    logger.info("==>>VIPUser update email:%s,expire:%s",buy_user,expire)
                                else:
                                    vipuser.update(is_vip=1,expire=(now + datetime.timedelta(days=365)))
                                    logger.info("==>>VIPUser update email:%s,now:%s,expire:%s",buy_user,now,expire)
                            else:
                                VIPUser.objects.create(email=buy_user,is_vip=1,expire=(now + datetime.timedelta(days=365)))
                                logger.info("==>>VIPUser create email:%s,expire:%s",buy_user,expire)
                        else:
                            vipuser = VIPUser.objects.filter(email=buy_user)
                            if vipuser:
                                myexpire = vipuser.values('expire')[0]['expire']
                                logger.info("myexpire:%s",myexpire)
                                if myexpire >= now:
                                    vipuser.update(is_vip=1,expire=(myexpire + datetime.timedelta(days=365)))
                                    logger.info("==>>VIPUser update email:%s,expire:%s",buy_user,expire)
                                else:
                                    vipuser.update(is_vip=1,expire=(now + datetime.timedelta(days=365)))
                                    logger.info("==>>VIPUser update email:%s,now:%s,expire:%s",buy_user,now,expire)
                            else:
                                VIPUser.objects.create(email=buy_user,is_vip=1,expire=(now + datetime.timedelta(days=365)))
                                logger.info("==>>VIPUser create email:%s,expire:%s",buy_user,expire)
                        logger.info("update successful==> out_trade_no:%s,trade_no%s",out_trade_no,trade_no)
                        return HttpResponse('success')
                    except Exception as e:
                        logger.debug("update fail==>out_trade_no:%s",e)
                        return HttpResponse('fail')
                else:
                    logger.info("out_trade_no:%s != order_id:%s",out_trade_no,order_id)
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
def order_result(request):
    now = datetime.datetime.now()
    product_info = ProductInfo.objects.all()
    t = request.POST.get('type','12')
    if t == '12':
        pid = product_info[0].id
        #name = u'SimpleNectVIP'
        name = product_info[0].name
        #desc = u'12个月'
        desc = product_info[0].desc
        #price = 0.01 
        price = product_info[0].price
    elif t == '6':
        pid = product_info[1].id
        #name = u'SimpleNectVIP'
        name = product_info[1].name
        #desc = u'6个月'
        desc = product_info[1].desc
        #price = 0.06
        price = product_info[1].price
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
        email = request.user.email
        number =1
        total_fee = number * price
        logger.info("buy_user:%s,order_id:%s,number:%s,total_fee:%s",email,order_id,number,total_fee)
        OrderInfo.objects.create(order_id=order_id,create_at=now,buy_user=email,buy_product_id=pid,number=1,total_fee=total_fee,pay_status=0)
    except Exception as e:
        logger.debug("order_result:%s",e)
    try:
        pay_url = create_direct_pay_by_user(order_id,name,desc,total_fee)
        logger.info("pay_url:%s",pay_url)
        #return HttpResponseRedirect(pay_url)
        return HttpResponseRedirect("/")
    except Exception as e:
        logger.debug("pay_url_debug:%s",e)
        raise Http404
        #return HttpResponseRedirect(pay_url)
     
