#_*_coding:utf-8_*_

import logging,json,os
from django.http import Http404
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

logger = logging.getLogger(__name__)

def index(request):
    data = {}
    posts =ForumPost.objects.all()
    for i in posts:
        comment = ForumComment.objects.filter(fid__exact=i).count()
        data[i] = comment
        #p = posts.filter(pk=i.pk)
    print data
    return render(request,"forum/index.html",{"posts":data})

def add(request):
    pass

def post(request,pid):
    post = ForumPost.objects.select_related().get(pk=pid)
    comments = post.forumcomment_set.all()
    return render(request,"forum/detail.html",{"post":post,"comments":comments})
