#_*_coding:utf-8_*_

from django.contrib import admin
from models import KxSoftAd
from forms import AdForm
import datetime

class AdAdmin(admin.ModelAdmin):
    now = datetime.datetime.now()
    ad = AdForm
    list_display =('title','ad_url','exp_day','create_time')
    fieldsets = (
        (None,{'fields':('title','ad_url','exp_day')}),
    )
    def save_model(self,request,obj,ad,change):
        obj.create_time = self.now
        obj.creater_id =request.user.uuid
        return super(AdAdmin, self).save_model(request, obj,ad, change)

admin.site.register(KxSoftAd,AdAdmin)
