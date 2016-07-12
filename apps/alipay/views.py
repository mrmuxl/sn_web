#_*_coding:utf-8_*_

import logging,uuid,time
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import (require_POST,require_GET)
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from models import OrderInfo
from lib.alipay import create_direct_pay_by_user


logger = logging.getLogger(__name__)

def return_url_handler(request):
    pass

def notify_url_handler(request):
    pass

def success(request):
    pass

def error(request):
    pass

@require_GET
@login_required
def order_info(request):
    return render(request,"alipay/order_result.html",{})

@require_POST
def order_result(request):
    order_id = time.strftime("%Y%m%d") + str(uuid.UUID.get_time_low(uuid.uuid1()))
    print order_id
    t = request.POST.get('type','12')
    if t == '12':
        name = u'SimpleNectVIP'
        desc = u'12个月'
        price = 1000 
    elif t == '6':
        name = u'SimpleNectVIP'
        desc = u'6个月'
        price = 600
    pay_url = create_direct_pay_by_user(order_id,name,desc,price)
    print pay_url
    #return HttpResponseRedirect(pay_url)
     
