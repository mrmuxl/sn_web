#_*_coding:utf-8_*_
import uuid,os,datetime,json,logging,time
from hashlib import md5
from base64 import urlsafe_b64encode,urlsafe_b64decode
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
from kx.models import KxUser,KxEmailInvate
from django.http import Http404
from django.core.mail import send_mail,EmailMultiAlternatives
from django.db import transaction

logger = logging.getLogger(__name__)

def save(request):
    now = datetime.datetime.now()
    word = [u'simplenect',u'运营',u'管理',u'系统']
    try:
        if request.method == "POST":
            email = request.POST.get('email','')
            nick = request.POST.get('nick','')
            password = request.POST.get('password','')
            repassword = request.POST.get('repassword','')
            if email and nick and password and repassword:
                email = strip_tags(email.strip().lower())
                nick = strip_tags(nick.strip())
                password = strip_tags(password.strip())
                repassword = strip_tags(repassword.strip())
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
                if nick in word:
                    message ="""昵称包含非法字符！<A HREF="javascript:history.back()">返 回</A>"""
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
                with transaction.commit_on_success():
                    try:
                        uid = md5(email).hexdigest()
                        create_user=KxUser.objects.create_user(id=uid,email=email,nick=nick,password=password,status=0)
                        #手贱的bug,auto_id不需要传None参数
                        create_user.save()
                        user = authenticate(username=email,password=password)
                        if user is not None and user.status == 0:
                            auth.login(request,user)
                            time_str = str(time.time())
                            email = str(email)
                            chk = md5(email + "," + time_str + ",qianmo20120601").hexdigest()
                            ver_data = email + "," + time_str + "," + chk
                            url =settings.DOMAIN + reverse('activate',args=[urlsafe_b64encode(ver_data),])
                            msg = "尊敬的SimpleNect用户，" + email + "：<br />&nbsp;&nbsp;您好！ <br />&nbsp;&nbsp;请点击以下链接激活您的账号：<a href='" + url + "'>" + url + "</    a>"
                            subject = '请激活帐号完成注册!'
                            from_email = 'SimpleNect <noreply@simaplenect.cn>'
                            mail = EmailMultiAlternatives(subject,msg,from_email,[email])
                            mail.content_subtype = "html"
                            mail.send(fail_silently=True)
                            return HttpResponseRedirect('/User/account_verify/?email='+email)
                        else:
                            message = """创建用户出现错误！<A HREF="javascript:history.back()">返 回</A>"""
                            return HttpResponse(message)
                    except Exception as e:
                        logger.debug("%s",e)
                        message = """邮件发送错误！<A HREF="javascript:history.back()">返 回</A>"""
                        return HttpResponse(message)
            else:
                message = """出现错误！?<A HREF="javascript:history.back()">返 回</A>"""
                return HttpResponse(message)
        else:
            return HttpResponseRedirect(reverse("index"))    
    except Exception as e:
        logger.debug("%s",e)
        #raise Http404

def login(request):
    '''登陆视图'''
    try:
        if request.method == "POST":
            email = strip_tags(request.POST.get("email",'').lower().strip())
            password = request.POST.get("password").strip()
            user = authenticate(username=email,password=password)
            if user and user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect(reverse("index"))    
            else:
                data={"email":email}
                messages.add_message(request,messages.INFO,_(u'用户名或密码错误'))
                return render(request,"login.html",data)
        return render(request,"login.html",{})
    except Exception as e:
        logger.debug("%s",e)
        raise Http404



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
@transaction.commit_on_success()
def avatar(request):
    date =datetime.date.strftime(datetime.date.today(),"%Y/%m/%d")
    uid = uuid.UUID.time_low.fget(uuid.uuid4())
    if request.method == "POST":
        image = request.FILES.get("avatar",None)
        folder = "User/"+str(date)
        if image:
            ext = str(image.content_type).split("/")[-1:][0]
            if ext in ('png','jpeg','gif','bmp'):
                file_name = image.name.encode('utf-8')
                file_size = str(image.size)
                file_uid = str(uid) 
                path_root = settings.MEDIA_ROOT
                path_folder = path_root + "/" + folder
                path_upload = path_folder + "/" + file_uid + "." +ext
                path_save = path_folder + "/" + file_uid + ".jpg"
                save_50 = path_folder + "/" + 'snap_50X50_' + file_uid + '.jpg'
                save_60 = path_folder + "/" + 'snap_60X60_' + file_uid + '.jpg'
                avatar_info = 'folder='+ folder + ',uid=' + file_uid + ',ext=jpg' + ',swidth=50,sheight=50' + ',name=' +file_name +',size=' + file_size
                try:
                    if not os.path.isdir(path_folder):
                        os.makedirs(path_folder)
                    try:
                        with open(path_upload,'wb') as fd:
                            for chunk in image.chunks():
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
    try:
        if request.method == 'GET':
            invate_code = request.GET.get('invate_code','')
            if invate_code and isinstance(invate_code,unicode):
                try:
                    invate_code = invate_code.strip().strip('\t').strip('\n').strip('\r').strip('\0').strip('\x0B')
                except Exception as e:
                    invate_code = '' 
                    logger.debug("%s",e)
            try:
                invate_obj = KxEmailInvate.objects.get(invate_code=invate_code)
                if invate_obj.id:
                    email = invate_obj.invate_email
                logger.info("%s",invate_obj)
            except Exception as e:
                email = ''
                invate_obj = []
                logger.debug("%s",e)
            temp_var = {
                        'invate_code':invate_code,
                        'email':email,
                    }
            return render_to_response("register.html",temp_var,context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(reverse("register"))
    except Exception as e:
        logger.debug("%s",e)
        raise Http404
        
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

def chpasswd(request):
    if request.method =="POST":
        oldPwd = request.POST.get("oldPwd","")
        pwd = request.POST.get("password","")
        repwd = request.POST.get("repassword","")
        status =1
        code = 0
        oldMsg = 0
        if not oldPwd:
            status = 0
            oldMsg = 1
        if not pwd:
            status = 0
            pwd = 0
        elif repwd != pwd:
            status = 0
            repwd = 0
        if status:
            try:
                user_obj = KxUser.objects.get(id=request.user.id)
                if md5(oldPwd).hexdigest() == user_obj.password:
                    try:
                        user_pwd = KxUser.objects.filter(id=user_obj.id).update(password=md5(pwd).hexdigest())
                        code =1
                    except Exception as e:
                        logger.debug("%s",e)
                else:
                    oldMsg =2
            except user_obj.DoesNotExist:
                logger.debug("%s",e)
                raise Http404
        if oldMsg > 0:
            oldMsg = oldMsg
        else:
            oldMsg = ''
        t_var ={
             'code':code,
            }
        return render(request,"changePwd.html",t_var)
    else:
        return render(request,"changePwd.html",{})

def findPwd(request):
    pass

def protocol(request):
    t_var ={
                'title':u'用户协议',
            }
    return render(request,"protocol.html",t_var)

@login_required
def to_active(request):
        if request.method =="GET":
            try:
                user_obj = KxUser.objects.get(id=request.user.id)
                try:
                    if user_obj.id and user_obj.status == 1:
                        messages.add_message(request,messages.INFO,_(u'此用户已激活!'))
                        return render(request,"to_active.html",{})
                    else:
                        time_str = str(time.time())
                        email = str(user_obj.email)
                        chk = md5(email + "," + time_str + ",qianmo20120601").hexdigest()
                        ver_data = email + "," + time_str + "," + chk
                        url =settings.DOMAIN + reverse('activate',args=[urlsafe_b64encode(ver_data),])
                        msg = "尊敬的SimpleNect用户，" + email + "：<br />&nbsp;&nbsp;您好！ <br />&nbsp;&nbsp;请点击以下链接激活您的账号：<a href='" + url + "'>" + url + "</a>"
                        subject = '请激活帐号完成注册!'
                        from_email = 'SimpleNect <noreply@simaplenect.cn>'
                        mail = EmailMultiAlternatives(subject,msg,from_email,[email])
                        mail.content_subtype = "html"
                        mail.send(fail_silently=True)
                        #send_mail(subject,msg,from_email,[email])
                        return HttpResponseRedirect('/User/account_verify/?email='+email)
                except Exception as e:
                    logger.debug("%s",e)
                    raise Http404
            except Exception as e:
                logger.debug("%s",e)
                messages.add_message(request,messages.INFO,_(u'激活邮件发送失败!'))
                return render(request,"to_active.html",{})
        else:
            raise Http404

def account_verify(request):
    try:
        if request.method =="GET":
            email = request.GET.get('email','')
            if email and isinstance(email,unicode):
                try:
                    email = email.strip().strip('\t').strip('\n').strip('\r').strip('\0').strip('\x0B')
                except Exception as e:
                    email = ''
                    logger.debug("%s",e)
                email_suffix = email.split('@')[1]
                email_login ='http://mail.' + email_suffix
            else:
                try:
                    email = request.user.email
                    email_suffix = email.split('@')[1]
                    email_login ='http://mail.' + email_suffix
                except Exception as e:
                    email = ''
                    logger.debug("%s",e)
                    message = """注册邮箱不存在！<A HREF="javascript:history.go(-2)">返 回</A>"""
                    return HttpResponse(message)

                
            t_var={
                    'email':email,
                    'email_login':email_login,
                }
            return render(request,"account_verify.html",t_var)
        else:
            return HttpResponseRedirect(reverse("register"))
    except Exception as e:
        logger.debug("%s",e)
        raise Http404

def activate(request,ver_data):
    try:
        now = time.time()
        active_time = datetime.datetime.now()
        ver_data = urlsafe_b64decode(str(ver_data)).split(',')
        email = ver_data[0]
        time_str = ver_data[1]
        md5_str = ver_data[2]
        chk = md5(email + "," + time_str + ",qianmo20120601").hexdigest()
        if md5_str == chk:
            if float(time_str)+24*3600 > now:
                try:
                    user_obj = KxUser.objects.filter(email=email).update(status=1,active_time=active_time)
                    return HttpResponseRedirect(reverse("verify_success"))
                except Exception as e:
                    logger.debug("%s",e)
                    message = """激活失败！<A HREF="javascript:history.back()">返 回</A>"""
                    return HttpResponse(message)
            else:
                message = """链接已失效！<A HREF="javascript:history.back()">返 回</A>"""
                return HttpResponse(message)
        else:
            message = """链接错误！<A HREF="javascript:history.back()">返 回</A>"""
            return HttpResponse(message)
    except Exception as e:
        logger.debug("%s",e)

def verify_success(request):
    return render(request,"verify_success.html",{})
