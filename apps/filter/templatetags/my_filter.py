#_*_coding:utf-8_*_
from django.conf import settings
from django import template 
register = template.Library()

@register.filter
def getDict(d,key):
	try:
		value=d[key]
	except KeyError:
		value=settings.TEMPLATE_STRING_IF_INVALID
	return value