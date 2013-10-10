#_*_coding:utf-8_*_

import logging,json,os
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_POST,require_GET)
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from apps.kx.models import KxUserlogin
from django.conf import settings
from pprint import pprint
from datetime import datetime
from models import ForumPost,ForumComment
from forms import ForumPostForm,ForumCommentForm

logger = logging.getLogger(__name__)

def index(request):
    data = [] 
    posts =ForumPost.objects.all().order_by('-created')
    for i in posts:
        comment = ForumComment.objects.filter(fid__exact=i).count()
        vote = i.vote_up-i.vote_down
        data.append((i, comment,vote))
    return render(request,"forum/index.html",{"posts":data})

@require_POST
@login_required(redirect_field_name='forum_index')
def add(request):
    form = ForumPostForm(request.POST)
    if form.is_valid():
        f = form.save(commit=False)
        f.user_id=request.user.pk
        f.save()
    return HttpResponseRedirect(reverse('forum_index'))  

@require_POST
@login_required(redirect_field_name="forum_add")
def reply(request):
    form = ForumCommentForm(request.POST)
    if form.is_valid():
        fid =form.cleaned_data['fid']
        f = form.save(commit=False)
        f.user_id=request.user.pk
        f.ip = request.META.get('REMOTE_ADDR','')
        f.save()
    return HttpResponseRedirect('post/'+str(fid)+'/')  

@require_GET
def post(request,pid):
    post = ForumPost.objects.select_related().get(pk=pid)
    vote = post.vote_up - post.vote_down
    comments = post.forumcomment_set.all()
    return render(request,"forum/detail.html",{"post":post,"vote":vote,"comments":comments})

@login_required()
@require_POST
def vote(request):
    message = {}
    pid = request.POST.get("id","")
    v = request.POST.get("v","")
    try:
        p = ForumPost.objects.get(pk=pid) 
        if v == '0':
            vote = p.vote_up + 1
            ForumPost.objects.filter(pk=pid).update(vote_up=vote) 
        elif '1'== v:
            vote = p.vote_down + 1
            ForumPost.objects.filter(pk=pid).update(vote_up=vote) 
        message['status']=1
        message['info']="投票成功!"
        message['data']=0
    except Exception as e:
        logger.debug("vote:%s",e)
        message['status']=0
        message['info']="投票失败!"
        message['data']=0
    return HttpResponse(json.dumps(message),content_type="application/json")


