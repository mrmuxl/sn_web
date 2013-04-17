#_*_coding:utf-8_*_
import uuid,os,datetime,json,logging
from hashlib import md5
from PIL import Image
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib import messages
from django.core.urlresolvers import reverse
from kx.utils import is_valid_email
from django.utils.html import strip_tags
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from kx.models import KxUser
from django.http import Http404

logger = logging.getLogger(__name__)

def save(request):
    now = datetime.datetime.now()
    info = "Data save success"
    try:
        if request.method == "POST":
            email = strip_tags(request.POST.get("email").strip().lower())
            nick = strip_tags(request.POST.get("nick").strip())
            password = request.POST.get("password").strip()
            repassword = request.POST.get("repassword").strip()
            if email is not None and nick is not None and password is not None and repassword is not None:
                if not email:
                    message ="""请填写邮箱！<A HREF="javascript:history.back()">返 回</A>"""
                    return HttpResponse(message)
                if not is_valid_email(email):
                    message ="""邮箱格式不正确！<A HREF="javascript:history.back()">返 回</A>"""
                    return HttpResponse(message)
                if not nick:
                    message ="""请填昵称！<A HREF="javascript:history.back()">返 回</A>"""
                    return HttpResponse(message)
                if len(nick)<4 and len(nick)>12:
                    message ="""昵称应为4-12个字符！<A HREF="javascript:history.back()">返 回</A>"""
                    return HttpResponse(message)
                if not password:
                    message ="""请填写密码！<A HREF="javascript:history.back()">返 回</A>"""
                    return HttpResponse(message)
                if password != repassword:
                    message ="""两次密码填写不一致！<A HREF="javascript:history.back()">返 回</A>"""
                    return HttpResponse(message)
                count = KxUser.objects.filter(email=email).count()
                if count >0:
                    message = """邮箱已存在！<A HREF="javascript:history.back()">返 回</A>"""
                    return HttpResponse(message)
                uid = md5(email).hexdigest()
                try:
                    #raise "aaa"
                    create_user=KxUser.objects.create_user(auto_id=None,id=uid,email=email,nick=nick,password=password,status=0)
                    create_user.save()
                    user = authenticate(username=email,password=password)
                except Exception as e:
                    logger.debug("%s",e)
                    return HttpResponseRedirect(reverse("login"))    
                if user is not None and user.is_active:
                    auth.login(request,user)
                    return HttpResponseRedirect(reverse("index"))    
        else:
            return HttpResponseRedirect(reverse("index"))    
    except Exception as e:
        logger.debug("%s",e)
        return HttpResponseRedirect(reverse("index"))    

def login(request):
    '''登陆视图'''
    if request.method == "POST":
        email = strip_tags(request.POST.get("email").lower().strip())
        password = request.POST.get("password").strip()
        user = authenticate(username=email,password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            return HttpResponseRedirect(reverse("index"))    
        else:
            data={"email":email}
            messages.add_message(request,messages.INFO,_(u'用户名或密码错误'))
            return render(request,"login.html",data)
    return render(request,"login.html",{})



@login_required
def info(request):
    try:
        obj_avatar = KxUser.objects.filter(email=request.user.email).values('avatar')
        l = []
        if obj_avatar:
            for i in obj_avatar[0]['avatar'].split(','):
                l.append(i.split('='))
            avatar = dict(l)
            logger.info('%s',avatar)
    except Exception as e:
        avatar = {}
        logger.debug(u'加载用户头像失败！',e,exc_info=True)
    return render(request,"info.html",avatar)

@login_required
def avatar(request):
    date =datetime.date.strftime(datetime.date.today(),"%Y/%m/%d")
    uid = uuid.UUID.time_low.fget(uuid.uuid4())
    if request.method == "POST":
        file = request.FILES.get("avatar",None)
        folder = "User/"+str(date)
        if file:
            ext = str(file.content_type).split("/")[-1:][0]
            if ext in ('png','jpeg','gif','bmp'):
                file_name = file.name.encode('utf-8')
                file_size = str(file.size)
                file_uid = str(uid) 
                path_root = settings.MEDIA_ROOT
                path_folder = path_root + "/" + folder
                path_upload = path_folder + "/" + file_uid + "." +ext
                path_save = path_folder + "/" + file_uid + ".jpg"
                save_50 = path_folder + "/" + 'snap_50X50_' + file_uid + '.jpg'
                save_60 = path_folder + "/" + 'snap_60X60_' + file_uid + '.jpg'
                avatar_info = 'folder='+ folder + ',uid=' + file_uid + ',ext=jpg' + ',swidth=0,sheight=0' + ',name=' +file_name +',size=' + file_size
                try:
                    if not os.path.isdir(path_folder):
                        os.makedirs(path_folder)
                    try:
                        with open(path_upload,'wb') as fd:
                            for chunk in file.chunks():
                                fd.write(chunk)
                    except Exception as e:
                        logger.debug(u"图片上传失败！%s",e)
                    size_50 = (50,50)
                    size_60 = (60,60)
                    image = Image.open(path_upload)
                    if image.format == 'GIF':
                        image = image.convert('RGB')
                    image.save(path_save,format="jpeg",quality=100)
                    image.resize(size_50,Image.ANTIALIAS).save(save_50,format="jpeg",quality=95)
                    image.resize(size_60,Image.ANTIALIAS).save(save_60,format="jpeg",quality=95)
                    try:
                        avatar_obj = KxUser.objects.filter(email=request.user.email).update(avatar=avatar_info)
                    except Exception as e:
                        logger.debug(u"插入数据库失败！%s",e)
                    return HttpResponseRedirect(reverse("info"))
                except Exception as e:
                    logger.debug(u"压缩图片失败！%s",e)
                    return HttpResponse("""上传文件失败请重新上传！<A HREF="javascript:history.back()">返 回</A>""")
            else:
                return HttpResponse("""不是支持的文件类型！<A HREF="javascript:history.back()">返 回</A>""")
        else:
            return HttpResponse("""请上传一张图片！<A HREF="javascript:history.back()">返 回</A>""")
    return HttpResponseRedirect(reverse("info"))

def register(request):
    '''注册视图'''
    return render_to_response("register.html",{},context_instance=RequestContext(request))
        
def check(request):
    if request.method =="POST":
        email = strip_tags(request.POST.get("email").strip().lower())
        if not email:
            return HttpResponse(json.dumps({"data":0,"info":"","status":0}),content_type="application/json")
        else:
            count = KxUser.objects.filter(email=email).count()
            if count == 0:
                return HttpResponse(json.dumps({"data":1,"info":"OK","status":1}),content_type="application/json")
    return HttpResponse(json.dumps({"data":0,"info":"","status":0}),content_type="application/json")


def logout(request):
    '''注销视图'''
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

def post(request):
    pass
def chpasswd(request):
    pass

