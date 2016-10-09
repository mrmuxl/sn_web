#_*_coding:utf-8_*_

from django.contrib import admin
from models import Forum,Category,Tag,Comment
from forms import ForumForm


class ForumAdmin(admin.ModelAdmin):
    def save_model(self,request,obj,forum,change):
        obj.author =request.user
        return super(ForumAdmin, self).save_model(request, obj,forum,change)


class CategoryAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    def save_model(self,request,obj,comment,change):
        obj.author =request.user
        return super(CommentAdmin, self).save_model(request, obj,comment,change)

admin.site.register(Tag,TagAdmin)
admin.site.register(Forum,ForumAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Comment,CommentAdmin)
