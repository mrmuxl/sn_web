#_*_coding:utf-8_*_

from django.contrib import admin
from models import ProductInfo,OrderInfo

class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('name','price','stocked')

class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ('order_id','create_at','buy_user','buy_product')

admin.site.register(ProductInfo,ProductInfoAdmin)
admin.site.register(OrderInfo,OrderInfoAdmin)
