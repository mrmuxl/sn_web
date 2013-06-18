#_*_coding:utf-8_*_

from django.conf import settings

def kx_settings(request):
    return {'DEBUG':settings.DEBUG,}
