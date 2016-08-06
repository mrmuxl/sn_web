#_*_coding:utf-8_*_
import logging
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from apps.client.decorators import snlogin_required
from django.shortcuts import render_to_response,render,get_object_or_404
from apps.sharefile.models import ShareFile, ShareFileSerializer
from django.shortcuts import get_object_or_404, render
from apps.kx.models import KxUser
from apps.online_user.models import OnlineUser

logger = logging.getLogger(__name__)


#打开与好友的聊天窗口
#@snlogin_required
def index(request):
	friendEmail = request.GET['email']

	friend = get_object_or_404(KxUser, email=friendEmail)

	return render(request, 'chat_index.html', {'friend':friend})
	#return render(request, 'chat_index.html')



#@snlogin_required
def sharefile(request):
	friendEmail = request.GET['email']

	friend = get_object_or_404(KxUser, email=friendEmail)

	return render(request, 'chat_sharefile.html', {'friend':friend})