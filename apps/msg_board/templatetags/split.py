#_*_coding:utf-8_*_

from django import template
register = template.Library()

@register.filter
def split(str,splitter):
    return str.split(splitter)
