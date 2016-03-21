#_*_coding:utf-8_*_
# Create your views here.

from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from kx.models import KxUser
from django.contrib.auth import authenticate
from django.contrib import auth,messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils import timezone
import json
import datetime
from django.views.decorators.csrf import csrf_exempt


def index(request):

    return render_to_response('index.html',{'title':u'首页',},context_instance=RequestContext(request))

from  django import forms

class myforms(forms.Form):
    """docstring for myforms"""
    subject = forms.CharField()



# def msg_board_1(request):
#     time_tag  = ' 23:59:59'
#     today = datetime.date.today()
#     last_month =str(today-datetime.timedelta(days=30))
#     left_create_time = last_month + time_tag
#     #right_create_time = str(today) + time_tag
#     right_create_time = '2013-03-1 23:59:59'
#     from django.db import connection, transaction
#     cursor = connection.cursor()
#     query="""SELECT * FROM kx_msg_board 
#               WHERE reply_id=0 AND is_del=0 AND '%s'  < create_time AND create_time < '%s' 
#               ORDER BY create_time DESC LIMIT 5;"""
#     cursor.execute(query %(str(left_create_time),str(right_create_time)))
#     msg_tuple=cursor.fetchall()
#     reply_ids = []
#     user_ids = []
#     for i in msg_tuple:
#         reply_id=i[0]
#         user_id=i[6]
#         if reply_id > 0:
#             reply_ids.append(str(reply_id))
#         if user_id > 0:
#             user_ids.append(user_id)


#     if reply_ids:
#         re_ids = ','.join(reply_ids)
#         reply_query="""SELECT id,reply_id,msg 
#                      FROM kx_msg_board 
#                      WHERE reply_id>0 AND is_del=0 AND reply_id IN (%s)
#                      ORDER BY create_time;"""
#         cursor.execute(reply_query %(re_ids))
#         re_tuple=cursor.fetchall()
#         reply_list = []
#         for i in re_tuple:
#             reid = i[1]
#             reply_list.append(reid)
             
#         # cursor.close()

def msg_board(request):
    req=request.session
    #print type(req)
    #print dir(req)
    #print req.keys()
    #print req.items()
    p=request.path
    u=request.user
    print dir(u)
    #print u.email


    return render(request,'msg_index.html',{'req':req,'p':p,'u':u}) 

def add_msg(request):
    return render(request,'msg_index.html',{}) 
def register(request):
    '''注册视图'''
#    now = timezone.now()
#    template_var={}
#    form = RegisterForm()    
#    if request.method=="POST":
#        form=RegisterForm(request.POST.copy())
#        if form.is_valid():
#            username=form.cleaned_data["username"]
#            email=form.cleaned_data["email"]
#            password=form.cleaned_data["password"]
#            user=KxUser.objects.create_user(username=username,email=email,password=password,create_time=now,update_time=now)
#            user.save()
#            _login(request,username,password)#注册完毕 直接登陆
#            return HttpResponseRedirect(reverse("index"))    
#    template_var["form"]=form        
    #print request
    return render_to_response("register.html",{},context_instance=RequestContext(request))
        

#@requires_csrf_token
#@csrf_exempt
def check(request):
    if request.method =="POST":
        email = request.POST.get("email")
        email = email.strip() 
        if not email:
            return HttpResponse(json.dumps({"data":0,"info":"","status":0}),content_type="application/json")
        else:
            count = KxUser.objects.filter(email=email).count()
            if count == 0:
                return HttpResponse(json.dumps({"data":1,"info":"OK","status":1}),content_type="application/json")
    return HttpResponse(json.dumps({"data":0,"info":"","status":0}),content_type="application/json")

 
def save(request):
    if request.method == "POST":
        email = request.POST.get("email").lower().strip()
        nick = request.POST.get("nick").strip()
        password = request.POST.get("password").strip()
        repassword = request.POST.get("repassword").strip()
        raw_email ="""请填写邮箱！<A HREF="javascript:history.back()">返 回</A>"""
        raw_nick ="""请填昵称！<A HREF="javascript:history.back()">返 回</A>"""
        raw_nick_length ="""昵称应为4-12个字符！<A HREF="javascript:history.back()">返 回</A>"""
        raw_password ="""请填写密码！<A HREF="javascript:history.back()">返 回</A>"""
        raw_repassword ="""两次密码填写不一致！<A HREF="javascript:history.back()">返 回</A>"""
        raw_has_email= """邮箱已存在！<A HREF="javascript:history.back()">返 回</A>"""
        if not email:
            return HttpResponse(raw_email)
        if not nick:
            return HttpResponse(raw_nick)
        if len(nick)<4 and len(nick)>12:
            return HttpResponse(raw_nick_length)
        if not password:
            return HttpResponse(raw_password)
        if password != repassword:
            return HttpResponse(raw_nick_length)
        count = KxUser.objects.filter(email=email).count()
        if count >0:
            return HttpResponse(raw_has_email)
        now = timezone.now()
        create_user=KxUser.objects.create_user(email=email,nick=nick,password=password,status=1)
        create_user.save()
        user = authenticate(username=email,password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            return HttpResponseRedirect(reverse("index"))    

def login(request):
    if request.method == "POST":
        email = request.POST.get("email").lower().strip()
        password = request.POST.get("password").strip()
        user = authenticate(username=email,password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            return HttpResponseRedirect(reverse("index"))    
        else:
            data={"email":email}
            messages.add_message(request,messages.INFO,_(u'用户名或密码错误'))
            return render(request,"login.html",data)
    return render(request,"login.html",{})

def logout(request):
    '''注销视图'''
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

#def info(request):
#    pass

def _login(request,email,password):
    '''登陆核心方法'''
    ret=False
    user=authenticate(username=email,password=password)
    if user is not None:
        if user.is_active:
            a=auth_login(request,user)
            ret=True
        else:
            messages.add_message(request, messages.INFO, _(u'用户没有激活'))
    else:
        messages.add_message(request, messages.INFO, _(u'用户不存在'))
    return ret
