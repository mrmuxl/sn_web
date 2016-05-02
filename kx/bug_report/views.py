#_*_coding:utf-8_*_
# Create your views here.

from django.http import Http404
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render_to_response,render
from django.http import HttpResponse, HttpResponseRedirect
from kx.models import (KxUser,KxMsgBoard,KxSoftRecord,KxTongjiRecord)
from django.contrib import auth,messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
import datetime,logging

logger = logging.getLogger(__name__)

def index(request):
    pass
