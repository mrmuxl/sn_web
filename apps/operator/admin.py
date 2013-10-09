#_*_coding:utf-8_*_

from django.contrib import admin
from models import Operator,OperatorAssistant,OperatorCategory


class OperatorAdmin(admin.ModelAdmin):
    pass

class OperatorCategoryAdmin(admin.ModelAdmin):
    pass

class OperatorAssistantAdmin(admin.ModelAdmin):
    pass


admin.site.register(Operator,OperatorAdmin)
admin.site.register(OperatorCategory,OperatorCategoryAdmin)
admin.site.register(OperatorAssistant,OperatorAssistantAdmin)
