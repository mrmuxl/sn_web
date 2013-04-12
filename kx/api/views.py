#_*_coding:utf-8_*_
import logging,json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def record(request):
    print request
    if request.method == 'POST':
        ver = request.POST.get('ver',None)
        cid = request.POST.get('clientIDentifie',None)
        md5str = request.POST.get('md5str',None)
        logger.info("%s:,%s:,%s:",ver,cid,md5str)
        if ver and cid and md5str:
            print ver,cid,md5str
            
        return HttpResponse(json.dumps({"data":0,"info":"","status":0}),content_type="application/json")
