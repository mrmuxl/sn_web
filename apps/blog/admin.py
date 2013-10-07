#_*_coding:utf-8_*_

from django.contrib import admin
from models import KxForumPosts,KxForumMpost,KxForumForum,Blog,Category
from forms import Posts,Mpost,Forums,BlogForm
import datetime

class PostsAdmin(admin.ModelAdmin):
    posts = Posts
    list_display =('title','create_time','update_time')
    list_display_links = ('title',)
    fieldsets = (
    #(u'添加文章',{'fields':('title','content','create_time','update_time')}),
    )
    def save_model(self,request,obj,posts,change):
        now = datetime.datetime.now()
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
        return super(ForumsAdmin, self).save_model(request, obj,forums, change)

class MpostAdmin(admin.ModelAdmin):
    mpost = Forums
    list_display = ('id','title','create_time','update_time')
    list_display_links = ('title',)


class BlogAdmin(admin.ModelAdmin):
    blog = BlogForm
    list_display =('title','author','created','modified')
    def save_model(self,request,obj,blog,change):
        obj.author =request.user
        return super(BlogAdmin, self).save_model(request, obj,blog, change)

class CategoryAdmin(admin.ModelAdmin):
    pass

#admin.site.register(KxForumPosts,PostsAdmin)
#admin.site.register(KxForumMpost,MpostAdmin)
#admin.site.register(KxForumForum,ForumsAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Category,CategoryAdmin)
