#_*_coding:utf-8_*_

from django.contrib import admin
from models import Spool
from forms import SpoolForm

class SpoolAdmin(admin.ModelAdmin):
    spoolform = SpoolForm
    list_display = ('uuid','origin_email','accept_email','printer_name','file_name','page_num','print_time','create_at','status','status_time')
    list_filter = ('status',)
admin.site.register(Spool,SpoolAdmin)
