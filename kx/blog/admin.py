#_*_coding:utf-8_*_

from django.contrib import admin
from models import KxForumPosts
from forms import AddPost


class AddPostAdmin(admin.ModelAdmin):
    add_form = AddPost
    list_display =('title',)
    fieldsets =(
    (u'添加文章',{'fields':('title','content')}),
    )
    
admin.site.register(KxForumPosts,AddPostAdmin)
