#_*_coding:utf-8_*_

from django.contrib import admin
from models import PublishUser,KxPub
from forms import PublishUserForm

class PublishUserAdmin(admin.ModelAdmin):
    publish_user = PublishUserForm
    list_display =('email','ver')

admin.site.register(PublishUser,PublishUserAdmin)
