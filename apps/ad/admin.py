#_*_coding:utf-8_*_

from django.contrib import admin
from models import KxSoftAd
from forms import AdForm

class AdAdmin(admin.ModelAdmin):
    ad = AdForm
    list_display =('title','ad_url','exp_day','create_time')
    def save_model(self,request,obj,ad,change):
        obj.creater_id =request.user.uuid
        return super(BlogAdmin, self).save_model(request, obj,ad, change)

admin.site.register(KxSoftAd,AdAdmin)
