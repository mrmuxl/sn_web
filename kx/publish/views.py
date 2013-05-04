#_*_coding:utf-8_*_
# Create your views here.

from django.http import Http404
from django.http import HttpResponse 
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from kx.models import KxSoftBug
from hashlib import md5
import datetime,logging,json,os

logger = logging.getLogger(__name__)

def publish_index(request):
    pass
def publish_add(request):
    pass
def publish_edit(request):
    pass
