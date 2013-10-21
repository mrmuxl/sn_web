#_*_coding:utf-8_*_

from django.contrib import admin
from models import Groups

class GroupsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Groups,GroupsAdmin)
