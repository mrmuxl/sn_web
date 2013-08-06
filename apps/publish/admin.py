#_*_coding:utf-8_*_

from django.contrib import admin
from models import PublishUser,KxPub
from forms import PublishUserForm

class PublishUserAdmin(admin.ModelAdmin):
    publish_user = PublishUserForm
    list_filter = ('is_publish','ver','repo_ver')
    list_display =('email','ver','repo_ver')
    search_fields = ('email',)
    ordering = ('-ver','-repo_ver','email')
    fieldsets = (
        (u'添加用户', {
            'classes': ('wide',),
            'fields': ('email', 'ver', 'repo_ver','is_publish')}
        ),
    )
    actions = ['make_published','make_unpublished']
    def make_published(self, request, queryset):
        rows_updated = queryset.update(is_publish=True)
        if rows_updated == 1:
            message_bit = "1 个用户"
        else:
            message_bit = "%s 个用户" % rows_updated
        self.message_user(request, u"%s 成功标记为已发布。" % message_bit)
    make_published.short_description = u"标记所选的用户为已发布"

    def make_unpublished(self, request, queryset):
        rows_updated = queryset.update(is_publish=False)
        if rows_updated == 1:
            message_bit = u"1 个用户"
        else:
            message_bit = u"%s 个用户" % rows_updated
        self.message_user(request, u"%s 成功标记为未发布。" % message_bit)
    make_unpublished.short_description = u"标记所选的用户为未发布"

admin.site.register(PublishUser,PublishUserAdmin)
