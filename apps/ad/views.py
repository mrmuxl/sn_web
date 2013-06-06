#_*_coding:utf-8_*_

import datetime,logging,json,os
from django.conf import settings
from django.http import Http404
from models import KxSoftAd
from django.views.decorators.http import (require_POST,require_GET)
#from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)

@require_GET
def ad_list(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('login'))
    else:
        try:
            ad_list = KxSoftAd.objects.order_by('-id').values()
            logger.info("%s",ad_list)
        except Exception as e:
            ad_list = []
            logger.debug("%s",e)
        t_var = {
                    'ad_list':ad_list,
                }
        return render(request,"ad/ad_list.html",t_var)
