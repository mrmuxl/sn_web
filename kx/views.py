#_*_coding:utf-8_*_
# Create your views here.

from django.http import Http404
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render_to_response,render
from django.http import HttpResponse, HttpResponseRedirect
from kx.models import (KxUser,KxMsgBoard,KxSoftRecord,KxTongjiRecord)
from django.contrib import auth,messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
import datetime,logging

logger = logging.getLogger(__name__)

def index(request):
    data={"title":u"首页"}
    time_tag  = ' 23:59:59'
    today = datetime.date.today()
    last_month =str(today-datetime.timedelta(days=30))
    left_create_time = last_month + time_tag
    #left_create_time = '2013-02-1 23:59:59'
    right_create_time = str(today) + time_tag
    #right_create_time = '2013-03-1 23:59:59'
    msg_count = KxMsgBoard.objects.filter(is_del__exact=0).count()
    data.update(msg_count=msg_count)
    msg_list = KxMsgBoard.objects.filter(reply_id__exact=0,is_del__exact=0,create_time__gte=left_create_time,create_time__lte=right_create_time).order_by("-create_time").values()[:5]
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
    return render(request,"index.html",data) 

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
                return HttpResponseRedirect(reverse("msg_show"))    
            else:
                try:
                    reply_create = KxMsgBoard.objects.create(ip=ip,msg=msg,create_time=create_time,reply_id=reply_id)
                except:
                    raise Http404
                return HttpResponseRedirect(reverse("msg_show"))    
        else:
            return HttpResponse(u'请填写留言内容！<A HREF="javascript:history.back()">返 回</A>')
    return HttpResponseRedirect(reverse("msg_show"))    


def post(request):
    pass
def chpasswd(request):
    pass
def tongji(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))
    else:
        try:
            login_num = KxUser.objects.extra(where=['DATE(last_login)=CURDATE()']).count()
            logger.info('login_num:%d',login_num)
        except Exception as e:
            login_num = 0
            logger.debug(u'用户呢?%s',e)
        try:
            all_user_num = KxSoftRecord.objects.filter(is_uninstall__exact=0).extra(select={'num':'count(DISTINCT client_identifie)'}).values('num')[0]['num']
            #all_user_num = KxSoftRecord.objects.extra(select={'num':'count(distinct client_identifie)'}).filter(is_uninstall__exact=0)
            logger.info('all_user_num:%s',all_user_num)
        except Exception as e:
            all_user_num =0
            logger.debug(u'有问题?%s',e)
        try:
            max_login = KxTongjiRecord.objects.order_by('-all_num').values('tongji_day','all_num')[:1]
            logger.info('max_login:%s',max_login)
        except Exception as e:
            max_login =0
            logger.debug(u'问题在那里?%s',e)
        today = datetime.date.today()
        if request.method == 'GET':
            tp = request.GET.get('type',1)
            day = request.GET.get('day',today)
            logger.info('type:%s day:%s',tp,day)
        temp_var={
                'title':u'统计',
                'login_num':login_num,
                'all_user_num':all_user_num,
                'type':tp,
                'day':day,
                }

        return render(request,"tongji.html",temp_var)

def login_tongji(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request,"login_tongji.html",{})

