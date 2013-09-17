#_*_coding:utf-8_*_

from django.contrib import admin
from models import Spool
from forms import SpoolForm

class SpoolAdmin(admin.ModelAdmin):
    spoolform = SpoolForm
admin.site.register(Spool,SpoolAdmin)
