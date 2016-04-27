#_*_coding:utf-8_*_
# Create your views here.

from django.http import Http404
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render_to_response,render
from django.http import HttpResponse, HttpResponseRedirect
from kx.models import (KxUser,KxMsgBoard)
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.html import strip_tags
import datetime,logging

logger = logging.getLogger(__name__)

def msg_board(request):
    data={"title":u"留言板"}
    time_tag  = ' 23:59:59'
    today = datetime.date.today()
    last_month =str(today-datetime.timedelta(days=30))
    #left_create_time = last_month + time_tag
    left_create_time = '2013-01-1 23:59:59'
    right_create_time = str(today) + time_tag
    #right_create_time = '2013-03-1 23:59:59'
    msg_list = KxMsgBoard.objects.filter(reply_id__exact=0,is_del__exact=0,create_time__gte=left_create_time,create_time__lte=right_create_time).order_by("-create_time").values()[:20]
    data.update(msg_list=msg_list)
    reply_ids = []
    user_ids = []
    for i in msg_list:
        if i['id'] >0:
            reply_ids.append(i['id'])
        if i['user_id'] >0:
            user_ids.append(i['user_id'])
    if reply_ids:
        try:
            reply_list = KxMsgBoard.objects.filter(is_del__exact=0,reply_id__gt=0,reply_id__in=reply_ids).order_by("create_time").values('id','reply_id','msg')
        except:
            raise Http404
        reply_dict={}
        for r in reply_list:
            reply_dict[r["id"]] = r
        data.update(reply_list=reply_dict)
    if user_ids:
        user_list = KxUser.objects.filter(id__in=user_ids).values('id','avatar')
        u_dict={}
        ul = []
        for u in user_list:
            if u['avatar']:
                ul.append([u"id",u['id']])
                for l in u['avatar'].split(','):
                    ul.append(l.split('='))
            user_dict=dict(ul)    
            if user_dict:
                u_dict[u['id']]=user_dict
            ul=[]
        data.update(user_list=u_dict)
    return render(request,"msg_index.html",data) 

def add_msg(request):
    if request.method =="POST":
        msg = strip_tags(request.POST.get("msg").strip()).strip()
        ip = request.META.get('REMOTE_ADDR','')
        create_time = datetime.datetime.now()
        reply = request.POST.get("reply")
        if msg:
            if reply is not None:
                try:
                    reply_id = int(strip_tags(reply.strip()))
                except ValueError:
                    raise Http404
                if reply_id and reply_id > 0:
                    reply_find = KxMsgBoard.objects.filter(reply_id__exact=reply_id).values('id','reply_id')
                    for i in reply_find:
                        if i['reply_id'] and i['reply_id'] == reply_id:
                            pass
                        else:
                            return HttpResponse(u'您要回复的留言不存在！<A HREF="javascript:history.back()">返 回</A>')
            else:
                reply_id = 0
            if request.user.is_authenticated() and not request.user.is_anonymous():
                user_id = request.user.id
                user_nick = request.user.nick
                try:
                    reply_create = KxMsgBoard.objects.create(ip=ip,msg=msg,create_time=create_time,reply_id=reply_id,user_id=user_id,user_nick=user_nick)
                except:
                    raise Http404
                return HttpResponseRedirect(reverse("msg_index"))    
            else:
                try:
                    reply_create = KxMsgBoard.objects.create(ip=ip,msg=msg,create_time=create_time,reply_id=reply_id)
                except:
                    raise Http404
                return HttpResponseRedirect(reverse("msg_index"))    
        else:
            return HttpResponse(u'请填写留言内容！<A HREF="javascript:history.back()">返 回</A>')
    return HttpResponseRedirect(reverse("msg_index"))    

def del_msg(request):
    pass

