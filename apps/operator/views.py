#_*_coding:utf-8_*_

import logging,json,os
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_POST,require_GET)
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from apps.kx.models import KxUserlogin
from django.conf import settings
from pprint import pprint
from datetime import datetime
from models import OperatorCategory,Operator,OperatorAssistant

logger = logging.getLogger(__name__)

