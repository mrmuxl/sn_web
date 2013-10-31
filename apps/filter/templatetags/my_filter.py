#_*_coding:utf-8_*_
from django.conf import settings
from django import template 
register = template.Library()

@register.filter
def getDict(d,key):
	if not isinstance(d, dict):
		return settings.TEMPLATE_STRING_IF_INVALID
	try:
		value=d[key]
	except KeyError:
		value=settings.TEMPLATE_STRING_IF_INVALID
	return value

@register.filter
def getAvatar(img,size=False):
	"""img 图片信息 size图片尺寸 如：50X60 """
	#folder=User/2012/08/10,uid=1862768215,ext=jpg,swidth=0,sheight=0,name=000.jpg,size=2541
	if img is None:
		return ""
	imgMsg=img.split(",")
	if len(imgMsg)!=7:
		return ""
	folder=imgMsg[0][7:]
	name=imgMsg[1][4:]+"."+imgMsg[2][4:]
	if size:
		return folder+"/snap_"+size+"_"+name
	return folder+"/"+name