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

@csrf_exempt
def upload_bug(request):
    message = {} 
    date =datetime.date.strftime(datetime.date.today(),"%Y/%m/%d")
    now = datetime.datetime.now()
    if request.method == 'POST':
        upload_file = request.FILES.get("mac",None)
        if upload_file:
            mac = upload_file.name.encode('utf-8')
            mac = mac.strip()
            mac_file =mac.replace(':','_') + ".dmp"
            folder = "/BugReport/"+str(date) + "/"
            path_root = settings.MEDIA_ROOT
            path_folder = path_root + folder
            path_upload = path_folder + mac_file
            new_file = mac_file
            try:
                if not os.path.isdir(path_folder):
                    os.makedirs(path_folder)
                try:
                    i=1
                    while 1:
                        if os.path.exists(path_folder + new_file):
                            i += 1
                            new_file = mac_file + '_' +str(i)
                        else:
                            break
                    with open(path_folder + new_file,'wb') as fd:
                        for chunk in upload_file.chunks():
                            fd.write(chunk)
                    message['message']=u"dump upload success文件上传成功!"
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                except Exception as e:
                    logger.debug(u"dump upload fail 1文件上传失败！%s",e)
                    message['message']=u"文件上传失败!"
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
            except Exception as e:
                logger.debug(u"文件上传失败！%s",e)
                message['message']=u"dump upload fail 2 文件上传失败!"
                message['create_time']=str(now)
                return HttpResponse(json.dumps(message),content_type="application/json")
        else:
            message['message']=u"dupm upload fail 3文件上传失败!"
            message['create_time']=str(now)
            return HttpResponse(json.dumps(message),content_type="application/json")
    
    
@csrf_exempt
def soft_bug(request):
    message = {} 
    now = datetime.datetime.now()
    if request.method == 'POST':
        email = request.POST.get('email','')
        ver = request.POST.get('ver','')
        client = request.POST.get('clientIdentifie','')
        md5str = request.POST.get('code','')
        os = request.POST.get('os','')
        auto_start = request.POST.get('autoStart','')
        lan_num = request.POST.get('lanNum','')
        if ver and client and md5str and os and auto_start and lan_num and email:
            email = email.strip()
            ver = ver.strip()
            client = client.strip()
            md5str = md5str.strip()
            os = os.strip()
            auto_start = auto_start.strip()
            lan_num = lan_num.strip()
            verify=md5(ver+client+'123456').hexdigest()
            if verify == md5str:
                try:
                    soft_bug_obj = KxSoftBug.objects.create(client_identifie=client,version=ver,upload_time=now,os=os,auto_start=auto_start,lan_num=lan_num,u_email=email)
                    message['message']=u"soft_bug interface ok!"
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                except Exception as e:
                    message['message']=u"soft_bug interface error!"
                    message['create_time']=str(now)
                    return HttpResponse(json.dumps(message),content_type="application/json")
                    logger.debug("%s",e)
                
@csrf_exempt
def bug_log(request):
    message = {} 
    now = datetime.datetime.now()
    date =datetime.date.strftime(datetime.date.today(),"%Y-%m-%d")
    path_root = settings.MEDIA_ROOT
    folder = "/BugLog/"+"soft_bug_" + str(date)  
    if request.method == 'POST':
        mac = request.POST.get('clientIdentifie','')
        log = request.POST.get('log','')
        if client and log:
            log_path = path_root + folder + '.log'
            log = mac + "   START*****************\n" + log + "\n" + mac  "   END*****************\n"
            with open(log_path,mode = 'a+',) as f:
                f.write(log)
            message['message']=u"bug_log ok!"
            message['create_time']=str(now)
            return HttpResponse(json.dumps(message),content_type="application/json")
        else:
            message['message']=u"bug_log ok!"
            message['create_time']=str(now)
            return HttpResponse(json.dumps(message),content_type="application/json")


