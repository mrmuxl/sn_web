#_*_coding:utf-8_*_
import logging
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from apps.client.decorators import sn_required
from django.shortcuts import render_to_response,render,get_object_or_404
from urllib import unquote
import md5

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
    logger.debug("rememberMe: asdfasdfasfas+++++++++++++++++++++++++")
    if request.method == "POST":
        request.session.clear()
        email = strip_tags(request.POST.get("email",'').lower().strip())
        rememberMe = request.POST.get('rememberMe', "-1")
        password = request.POST.get("password").strip()
        refer = request.POST.get("refer","")
        user = authenticate(username=email,password=password)
        logger.debug("rememberMe===================: %s", rememberMe)
        if user and user.is_active:
            auth.login(request,user)
            #登录成功，保存表单项到cookie

            response = HttpResponseRedirect("/client/friend/feed/") 
            response.set_cookie("email", email)
            response.set_cookie("rememberMe", rememberMe)
            if rememberMe == "1":
                logger.debug("rememberMe======true=============:true")
                response.set_cookie("sss1", password)
            else:
                response.delete_cookie("sss1")
            return response
        else:
            data={"email":email}
            messages.add_message(request,messages.INFO,_(u'用户名或密码错误'))
            return render(request, "client_login.html", data)

    elif request.method == "GET":
        email = request.COOKIES.get('email')
        rememberMe = request.COOKIES.get('rememberMe')
        password = request.COOKIES.get('sss1')
        if email:
            email = unquote(email)
        else:
            email = ""

        logger.debug("==================+ %s", rememberMe)
        if rememberMe is None:
            rememberMe = "1"
        logger.debug("==================++ %s", rememberMe)

        logger.debug("=======___===========++password %s", password)



        return render(request,"client_login.html", 
            {"email": email, "rememberMe": rememberMe})

