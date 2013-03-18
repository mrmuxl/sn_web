#_*_coding:utf-8_*_
# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import datetime
from django.contrib.auth import get_user_model
from kx.forms import RegisterForm
from kx.models import KxUser
from django.contrib.auth import authenticate
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils import timezone
import json


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
    print type(req)
    print dir(req)
    print req.keys()
    print req.items()
    p=request.path
    u=request.user

    return render(request,'msg_index.html',{'req':req,'p':p,'u':u}) 

def  add_msg(request):
    pass
def register(request):
    '''注册视图'''
#    now = timezone.now()
    template_var={}
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
    return render_to_response("register.html",template_var,context_instance=RequestContext(request))
    if request.method =="POST":
        username=request.POST["nick"]
        email=request.POST["nick"]
        

def check(request):
    print request
    if request.method =="POST":
        email = request.POST.get("email")
        email = email.strip() 
        print email
        if not email:
            return HttpResponse(json.dumps({"data":0,"info":"","status":0}),content_type="application/json")
        else:
            count = KxUser.objects.filter(email=email).count()
            print count
            if count == 0:
                return HttpResponse(json.dumps({"data":1,"info":"OK","status":1}),content_type="application/json")
    return HttpResponse(json.dumps({"data":0,"info":"","status":0}),content_type="application/json")

 
def save(request):
    pass


#def login(request):
#    pass
#def logout(request):
#    pass
#
#def info(request):
#    pass
#def _login(request,username,password):
#    '''登陆核心方法'''
#    ret=False
#    user=authenticate(username=username,password=password)
#    if user:
#        if user.is_active:
#            auth_login(request,user)
#            ret=True
#        else:
#            messages.add_message(request, messages.INFO, _(u'用户没有激活'))
#    else:
#        messages.add_message(request, messages.INFO, _(u'用户不存在'))
#    return ret
