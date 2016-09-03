#_*_coding:utf-8_*_

from django.contrib import admin
from models import ProductInfo,OrderInfo

class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('name','category','price','stocked')

class OrderInfoAdmin(admin.ModelAdmin):
    list_filter = ('pay_status',)
    list_display = ('order_id','buy_user','total_fee','create_at','buy_product','number','pay_status','pay_at','trade_no','status','auth_user_num')

admin.site.register(ProductInfo,ProductInfoAdmin)
admin.site.register(OrderInfo,OrderInfoAdmin)
