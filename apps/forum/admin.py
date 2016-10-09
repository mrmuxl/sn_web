#_*_coding:utf-8_*_

from django.contrib import admin
from models import ForumPost,ForumTags,ForumComment


class ForumPostAdmin(admin.ModelAdmin):
    def save_model(self,request,obj,forum,change):
        obj.author =request.user
        return super(ForumPostAdmin, self).save_model(request, obj,forum,change)


#class ForumCategoryAdmin(admin.ModelAdmin):
#    pass

class ForumTagsAdmin(admin.ModelAdmin):
    pass

class ForumCommentAdmin(admin.ModelAdmin):
    def save_model(self,request,obj,comment,change):
        obj.author =request.user
        return super(ForumCommentAdmin, self).save_model(request, obj,comment,change)

admin.site.register(ForumTags,ForumTagsAdmin)
admin.site.register(ForumPost,ForumPostAdmin)
#admin.site.register(ForumCategory,ForumCategoryAdmin)
admin.site.register(ForumComment,ForumCommentAdmin)
