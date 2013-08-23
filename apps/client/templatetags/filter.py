#_*_coding:utf-8_*_
from __future__ import unicode_literals
import re
from datetime import date, datetime
from decimal import Decimal

from django import template
from django.conf import settings
from django.template import defaultfilters
from django.utils.encoding import force_text
from django.utils.formats import number_format
from django.utils.translation import pgettext, ungettext, ugettext as _
from django.utils.timezone import is_aware, utc
from django import template


register = template.Library()

@register.filter
def afterLast(str, val):
    return str.split(val)[-1]



@register.filter
def naturaltime(value):
    """
    For date and time values shows how many seconds, minutes or hours ago
    compared to current timestamp returns representing string.
    """
    if not isinstance(value, date): # datetime is a subclass of date
        return value

    now = datetime.now(utc if is_aware(value) else None)
    if value < now:
        delta = now - value
        if delta.days > 7:
            return defaultfilters.date(value, "m-d H:i")
        elif delta.days > 0 and delta.days <= 7:
            return  "%i天前" % delta.days
        elif delta.seconds < 60:
            return "刚刚"
        elif delta.seconds // 60 < 60:
            count = delta.seconds // 60
            return "%i分钟前" % count
        else:
            count = delta.seconds // 60 // 60
            return "%i小时前" % count



