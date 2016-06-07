#_*_coding:utf-8_*_
import logging
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from apps.client.decorators import sn_required
from django.shortcuts import render_to_response,render,get_object_or_404

logger = logging.getLogger(__name__)

@csrf_exempt
@sn_required
def silencelogin(request):
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



@sn_required
def login(request):
    '''登陆视图'''
    if request.method == "POST":
        email = strip_tags(request.POST.get("email",'').lower().strip())
        password = request.POST.get("password").strip()
        rememberMe = request.POST.get("rememberMe",'').lower().strip()
        refer = request.POST.get("refer","")
        user = authenticate(username=email,password=password)
        logger.debug("rememberMe: %s",rememberMe)
        if user and user.is_active:
            auth.login(request,user)
            if rememberMe:
                request.session.set_expiry(0)
            return HttpResponseRedirect(reverse("client.friend.feed"))    
        else:
            data={"email":email}
            messages.add_message(request,messages.INFO,_(u'用户名或密码错误'))
            return render(request, "client_login.html", data)

    elif request.method == "GET":
        return render(request,"client_login.html",{})

