#_*_coding:utf-8_*_

import logging
from django.views.decorators.http import (require_POST,require_GET)
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render


logger = logging.getLogger(__name__)

def index(request):
    return render(request,"alipay/index.html",{})

def return_url_handler(request):
    pass

def notify_url_handler(request):
    pass

def success(request):
    pass

def error(request):
    pass

@require_POST
def order_result(request):
    t = request.POST.get('order_type','')
    return render(request,"alipay/order_result.html",{})
