#_*_coding:utf-8_*_
import logging
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from apps.client.decorators import sn_required

logger = logging.getLogger(__name__)

@csrf_exempt
@sn_required
def login(request):
    '''登陆视图'''
    if request.method == "POST":
        email = strip_tags(request.POST.get("email",'').lower().strip())
        password = request.POST.get("password").strip()
        user = authenticate(username=email,password=password)
        if user and user.is_active:
            auth.login(request,user)
            return HttpResponse("1")
        else:
            return HttpResponse("-1")
    else:
    	return HttpResponse("-2")
