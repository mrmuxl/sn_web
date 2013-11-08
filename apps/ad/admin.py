#_*_coding:utf-8_*_

from django.contrib import admin
from models import KxSoftAd
from forms import AdForm
from datetime import datetime
from models import Operator,OperatorAssistant,OperatorCategory

class OperatorInline(admin.StackedInline):
    model = Operator

class AdAdmin(admin.ModelAdmin):
    now = datetime.now()
    ad = AdForm
    list_display =('title','ad_url','exp_day','create_time')
    fieldsets = (
        (None,{'fields':('title','ad_url','exp_day')}),
    )
    def save_model(self,request,obj,ad,change):
        obj.create_time = self.now
        obj.creater_id =request.user.uuid
        return super(AdAdmin, self).save_model(request, obj,ad, change)

class OperatorAdmin(admin.ModelAdmin):
    list_display =('category','user','name','printer_num','used_num','qq','tel','school','created','expire','status')

class OperatorCategoryAdmin(admin.ModelAdmin):
    pass

class OperatorAssistantAdmin(admin.ModelAdmin):
    pass

admin.site.register(KxSoftAd,AdAdmin)
admin.site.register(Operator,OperatorAdmin)
admin.site.register(OperatorCategory,OperatorCategoryAdmin)
admin.site.register(OperatorAssistant,OperatorAssistantAdmin)
