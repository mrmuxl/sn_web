#_*_coding:utf-8_*_
import logging
from django.shortcuts import render
from django.views.decorators.http import require_GET
from models import (KxForumMpost,KxForumPosts,Blog)

logger = logging.getLogger(__name__)

def show(request):
    query="""select m.id,m.forum_id,m.title,m.reply_num,m.view_num,m.create_time,p.content from kx_forum_mpost m left join kx_forum_posts p on m.id=p.tid where m.is_del=0 and p.is_main=1  order by m.top_num desc,id desc"""
    try:
        post_show = KxForumMpost.objects.raw(query)
    except Exception as e:
        post_show =''
        logger.debug("%s",e)
    t_var = {
                'title':u"新手指南",
                'post_show':post_show
            }
    return render(request,"blog/show.html",t_var)

@require_GET
def help(request):
    return render(request,"blog/help.html",{})

@require_GET
def blog_index(request):
    posts = Blog.objects.all()
    top = [ i for i in posts if i.is_top == 1 and i.status == 0]
    page = [ i for i in posts if i.is_top == 0 and i.status == 0]
    t_var = {
                'title':u"新手指南",
                'top':top,
                'page':page,
            }
    return render(request,"blog/show.html",t_var)
    
