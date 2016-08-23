#_*_coding:utf-8_*_
# Create your views here.

from django.http import Http404
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render_to_response,render
from django.http import HttpResponse, HttpResponseRedirect
from apps.kx.models import (KxUser,KxMsgBoard,KxSoftRecord,KxTongjiRecord)
from apps.publish.models import KxPub
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
    try:
        msg_count = KxMsgBoard.objects.filter(is_del__exact=0).count()
        msg_list = KxMsgBoard.objects.filter(reply_id__exact=0,is_del__exact=0,create_time__gte=left_create_time,create_time__lte=right_create_time).order_by("-create_time").values()[:5]
        logger.info("msg_count:%s",msg_count)
    except Exception as e:
        msg_count = 0
        msg_list = ''
        logger.debug("%s",e)
    data.update(msg_count=msg_count)
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
        user_list = KxUser.objects.filter(uuid__in=user_ids).values('uuid','avatar')
        u_dict={}
        ul = []
        for u in user_list:
            if u['avatar']:
                ul.append([u"uuid",u['uuid']])
                for l in u['avatar'].split(','):
                    ul.append(l.split('='))
            user_dict=dict(ul)
            if user_dict:
                u_dict[u['uuid']]=user_dict
            ul=[]
        data.update(user_list=u_dict)
    try:
        ins_file = KxPub.objects.filter(pub_time__isnull=False).order_by('-id')[0:1].get()
        repo_file = KxPub.objects.filter(pub_time__isnull=False).order_by('-id')[1:2].get()
        data.update(repo_file=ins_file.install_file,ins_file=repo_file.install_file)
    except Exception as e:
        data.update(ins_file='')
        logger.debug("ins_file:%s",e)
    return render(request,"index.html",data) 

