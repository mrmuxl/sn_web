#_*_coding:utf-8_*_

from django.contrib import admin
from models import Spool
from forms import SpoolForm

class SpoolAdmin(admin.ModelAdmin):
    spoolform = SpoolForm
    list_filter = ('uuid','origin_email','origin_uuid','accept_email','accept_uuid','print_name','print_uuid','file_name','file_path','file_client_path','page_num','print_time','create_at','status','status_time')
admin.site.register(Spool,SpoolAdmin)
