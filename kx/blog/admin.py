#_*_coding:utf-8_*_

from django.contrib import admin
from models import KxForumPosts,KxForumMpost,KxForumForum
from forms import Posts,Mpost,Forums
import datetime


class PostsAdmin(admin.ModelAdmin):
    posts = Posts
    list_display =('title','create_time','update_time')
    fieldsets = (
    #(u'添加文章',{'fields':('title','content','create_time','update_time')}),
    )
    def save_model(self,request,obj,posts,change):
        print obj,dir(obj)
        print obj.id
        pass

class ForumsAdmin(admin.ModelAdmin):
    forums = Forums
    list_display =('name','update_time')
    fieldsets = (
    (u'添加分类',{'fields':('name',)}),
    )
    def save_model(self,request,obj,forums,change):
        now = datetime.datetime.now()
        obj.updater_id =request.user.uuid
        obj.update_time=now
        print dir(obj)
        print forums
        return super(ForumsAdmin, self).save_model(request, obj,forums, change)


admin.site.register(KxForumPosts,PostsAdmin)
admin.site.register(KxForumForum,ForumsAdmin)
