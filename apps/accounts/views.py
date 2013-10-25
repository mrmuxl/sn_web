#_*_coding:utf-8_*_

import uuid,os,datetime,json,logging,time,shutil
from hashlib import md5
from base64 import urlsafe_b64encode,urlsafe_b64decode
from PIL import Image
from django.contrib.auth import authenticate,REDIRECT_FIELD_NAME
from django.contrib import auth
from django.contrib import messages
from django.core.urlresolvers import reverse
from apps.kx.utils import is_valid_email,send_mail_thread
from django.utils.html import strip_tags
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response,render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST,require_GET
from django.conf import settings
from apps.kx.models import KxUser,KxEmailInvate,KxMailingAddfriend
from apps.kx.models import KxUserFriend,KxPub
from django.http import Http404
from django.db.models import Sum
#from django.core.mail import send_mail,EmailMultiAlternatives
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from utils import *
from django.utils.http import is_safe_url
from apps.spool.models import Spool
from apps.alipay.models import OrderInfo
from apps.ad.models import OperatorAssistant,Operator
from apps.kx.tongji.utils import CustomSQL
from apps.utils.json_util import *
from apps.accounts.service import *
from apps.msg_board.utils import uniqid,str_reverse,uniq

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
            send_from = request.POST.get("send_from")
            if send_from != u'1':
                uniq_id = str_reverse(send_from[0:13])[0:6]
                uiq = uniq()[0:6]
                if uniq_id == uiq:
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
                                create_user=KxUser.objects.create_user(uuid=uid,email=email,nick=nick,password=password,status=0)
                                create_user.save()
                                user = authenticate(username=email,password=password)
                                if user is not None and user.status == 0:
                                    auth.login(request,user)
                                    time_str = str(time.time())
                                    email = str(email)
                                    chk = md5(email + "," + time_str + ",qianmo20120601").hexdigest()
                                    ver_data = email + "," + time_str + "," + chk
                                    url =settings.DOMAIN + reverse('activate',args=[urlsafe_b64encode(ver_data),])
                                    msg = "尊敬的SimpleNect用户，" + email + "：<br />&nbsp;&nbsp;您好！ <br />&nbsp;&nbsp;请点击以下链接激活您的账号：<a href='" + url + "'>" + url + "</a>"
                                    subject = '请激活帐号完成注册!'
                                    from_email = 'SimpleNect <noreply@simaplenect.cn>'
                                    #mail = EmailMultiAlternatives(subject,msg,from_email,[email])
                                    #mail.content_subtype = "html"
                                    #mail.send(fail_silently=True)
                                    try:
                                        send_mail_thread(subject,msg,from_email,[email],html=msg)
                                        logger.info("active account:%s",email)
                                    except Exception as e:
                                        logger.debug("active account:%s",e)
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
                    message = """出现错误！?<A HREF="javascript:history.back()">返 回</A>"""
                    return HttpResponse(message)
            else:
                message = """出现错误！?<A HREF="javascript:history.back()">返 回</A>"""
                return HttpResponse(message)
        else:
            return HttpResponseRedirect(reverse("index"))    
    except Exception as e:
        logger.debug("%s",e)

def login(request,next_page="/User/index",redirect_field_name=REDIRECT_FIELD_NAME):
    '''登陆视图'''
    if request.method == "GET":
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')    
        #if redirect_field_name in request.REQUEST:
        #    next_page = request.REQUEST[redirect_field_name]
        if not is_safe_url(url=next_page, host=request.get_host()):
            next_page = "/"
        else:
            next_page = request.META.get("HTTP_REFERER","/User/index/")
            # Security check -- don't allow redirection to a different host.
            if not is_safe_url(url=next_page, host=request.get_host()):
                next_page = "/"
        if next_page:
            request.session['next_page'] = next_page
        return render(request,"login.html",{})
    elif request.method == "POST":
        email = strip_tags(request.POST.get("email",'').lower().strip())
        password = request.POST.get("password").strip()
        refer = request.POST.get("refer","")
        user = authenticate(username=email,password=password)
        if user and user.is_active:
            auth.login(request,user)
            rn = request.session.get('next_page','')
            if rn:
                if rn.replace("http://","") == request.get_host()+"/":
                    return HttpResponseRedirect(next_page)    
            return HttpResponseRedirect(request.session.get('next_page','/User/index/'))    
        else:
            data={"email":email}
            messages.add_message(request,messages.INFO,_(u'用户名或密码错误'))
            if not refer:
                return render(request,"login.html", data)
            else:
                request.session.set_expiry(0)
                return render(request, "client_login.html", data)


def register(request,invate_code=''):
    '''注册视图'''
    if invate_code:
        if isinstance(invate_code,unicode):
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
        t_var = {
                    'invate_code':invate_code,
                    'email':email,
                }
        return render(request,"register.html",t_var)
    else:
        return render(request,"register.html",{})
        
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

@login_required
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
                user_obj = KxUser.objects.get(uuid=request.user.uuid)
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
             'pwd':pwd,
             'repwd':repwd,
             'code':code,
             'oldMsg':oldMsg,
            }
        return render(request,"user/changePwd.html",t_var)
    else:
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
        return render(request,"user/changePwd.html",avatar)

def findPwd(request):
    step = 1
    if request.method =="POST":
        email = request.POST.get('email','')
        if email:
            code =0
            email = email.strip()
            try:
                user_obj = get_object_or_404(KxUser,email=email)
                if user_obj.id:
                    time_str = str(time.time())
                    chk = md5(email + "," + time_str + ",kx2011").hexdigest()
                    data = email + "," + time_str + "," + chk
                    url =settings.DOMAIN + reverse('resetPwd',args=[urlsafe_b64encode(data),])
                    msg =u"尊敬的用户，" + email + u"<br />&nbsp;&nbsp;您好！<br/>&nbsp;&nbsp;请点击以下链接重置密码：<a href='"+ url + "'>" + url + "</a>"
                    from_email = 'SimpleNect <noreply@simaplenect.cn>'
                    subject = "SimpleNect用户密码重置提示函"
                    try:
                        send_mail_thread(subject,msg,from_email,[email],html=msg)
                        logger.info("rest password:%s",email)
                        code =1
                        step =2
                    except Exception as e:
                        logger.debug("rest password:%s",e)
                        code = 2
                else:
                    code = 0
                t_var = { 'step':step, 'code':code, }
                return render(request,"findPwd.html",t_var)
            except Exception as e:
                logger.debug("%s",e)
                t_var = { 'step':step, 'code':code, }
                return render(request,"findPwd.html",t_var)
        else:
            t_var ={ 'step':step,}
            return render(request,"findPwd.html",t_var)
    else:
        t_var ={ 'step':step,}
        return render(request,"findPwd.html",t_var)

@require_GET
def resetPwd(request,verify):
    if verify:
        now = time.time()
        verify = urlsafe_b64decode(str(verify)).split(',')
        email = verify[0]
        time_str = verify[1]
        md5_str = verify[2]
        chk = md5(email + "," + time_str + ",kx2011").hexdigest()
        if md5_str == chk:
            if float(time_str)+24*3600 > now:
                chkcode = md5(email+"2011kx").hexdigest()
                t_var = {
                         'email':email,
                         'chkcode':chkcode,
                        }
                return render(request,"resetPwd.html",t_var)
            else:
                t_var ={'email':email,}
                messages.add_message(request,messages.INFO,_(u'链接已经失效'))
                return render(request,"resetPwd.html",t_var)
        else:
            t_var ={'email':email,}
            messages.add_message(request,messages.INFO,_(u'链接错误'))
            return render(request,"resetPwd.html",t_var)
    else:
        t_var ={'email':email,}
        messages.add_message(request,messages.INFO,_(u'链接非法'))
        return render(request,"resetPwd.html",t_var)

@require_POST
def rePwd(request):
    code = 0
    email = request.POST.get('email','')
    password = request.POST.get('password','')
    repassword = request.POST.get('repassword','')
    chkcode = request.POST.get('chkcode','')
    if  email and password and repassword and chkcode:
        email = email.strip()
        password = password.strip()
        repassword = repassword.strip()
        chkcode = chkcode.strip()
        chk = md5(email+"2011kx").hexdigest()
        if chk == chkcode and password == repassword:
            try:
                user_pwd = KxUser.objects.filter(email=email).update(password=md5(password).hexdigest())
                code =1 
            except Exception as e:
                logger.debug("%s",e)
                code = 2
        t_var = {
                  'email':email,
                  'code':code,
                  'chkcode':chkcode,
                }
        return render(request,"rePwd.html",t_var)


@require_GET
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
                        #mail = EmailMultiAlternatives(subject,msg,from_email,[email])
                        #mail.content_subtype = "html"
                        #mail.send(fail_silently=True)
                        send_mail_thread(subject,msg,from_email,[email],html=msg)
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

@require_GET
def account_verify(request):
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

@require_GET
def activate(request,ver_data):
    if ver_data:
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
    else:
        message = """链接非法！<A HREF="javascript:history.back()">返 回</A>"""
        return HttpResponse(message)

@require_GET
def verify_success(request):
    return render(request,"verify_success.html",{})

@csrf_exempt
@require_GET
def invite_msg(reqeust,ckey=''):
    key = '518279d14e20e'
    site_url = settings.DOMAIN
    reg_url = settings.DOMAIN + u'/User/register'
    sendok_ids = []
    mail_list = KxMailingAddfriend.objects.filter(is_sendemail__exact=0).values()
    if ckey and mail_list and key == ckey:
        for i in mail_list:
            invite_content = i['invite_content'].strip()
            from_email = i['user'].strip()
            to_email = i['friend'].strip()
            if not to_email:
                KxMailingAddfriend.objects.filter(id=i['id']).update(is_del=1,is_sendemail=1)
                continue
            try:
                user_obj = KxUser.objects.get(email=from_email)
                from_nick = user_obj.nick
            except Exception as e:
                from_nick = from_email
                logger.debug("invite_msg:%s",e)
            if i['send_reason_type'] == 0:
                subject = u'SimpleNect好友邀请信息！'
                msg = invite_register(from_nick,invite_content,reg_url)
                try:
                    send_mail_thread(subject,msg,from_email,[to_email],html=msg)
                    sendok_ids.append(str(i['id']))
                except Exception as e:
                    logger.debug("%s",e)
                break
            elif i['send_reason_type'] == 1:
                subject = u'SimpleNect好友邀请提示信息！'
                invite_content =u'希望加你为好友，请及时登录SimpleNect客户端，确认邀请信息。'
                msg = invite_register(from_nick,invite_content,reg_url)
                try:
                    send_mail_thread(subject,msg,from_email,[to_email],html=msg)
                    sendok_ids.append(str(i['id']))
                except Exception as e:
                    logger.debug("%s",e)
                break
            elif i['send_reason_type'] == 2:
                subject = u'SimpleNect好友邀请提示信息！'
                to_email = i['user'] 
                invite_content =u'通过了您的好友邀请，请登录SimpleNect客户端，现在你们可以进行通讯了。'
                msg = invite_register(from_nick,invite_content,reg_url)
                try:
                    send_mail_thread(subject,msg,from_email,[to_email],html=msg)
                    sendok_ids.append(str(i['id']))
                except Exception as e:
                    logger.debug("%s",e)
                break
            else:
                pass
        if sendok_ids:
            KxMailingAddfriend.objects.filter(id__in=sendok_ids).update(is_del=1,is_sendemail=1)
            logger.info("%s",sendok_ids)
        sendok ="<br/>".join(sendok_ids)
        return HttpResponse(sendok_ids)
    else:
        message = """Key Error or No email to send !<A HREF="javascript:history.back()">返 回</A>"""
        return HttpResponse(message)

@login_required
@require_GET
def index(request):
    now = datetime.datetime.now()
    print_count = Spool.objects.filter(origin_email=request.user.email).count()
    print_record = Spool.objects.filter(origin_email=request.user.email).order_by("-print_time")[0:5]
    my_printer = Spool.objects.filter(accept_email=request.user.email).order_by("-print_time")[0:5]
    #print_count = print_record.count()
    #print_record = Spool.objects.filter(origin_email='falqs@foxmail.com')
    #buy_user = OrderInfo.objects.filter(buy_user=request.user.email)
    my_friends = KxUserFriend.objects.filter(user=request.user.email).count()
    printer_num = Operator.objects.filter(user=request.user.pk).filter(status__exact=1).filter(expire__gt=now).values('printer_num','used_num','expire')
    if printer_num:
        expire_days = printer_num[0]['expire']
        remain_days = (expire_days - now).days
        p_num = printer_num[0]["printer_num"]
        used_num = printer_num[0]["used_num"]
    else:
        p_num =0
        used_num =0
        remain_days =0
    try:
        ins_file = KxPub.objects.filter(pub_time__isnull=False).filter(install_file__istartswith='SimpleNect_V').order_by('-id')[0:1].get()
        ins_file=ins_file.install_file
    except Exception as e:
        ins_file = ""
        logger.debug("ins_file:%s",e)
        
    try:
        q = """ select count(*) from kx_share where owner_email=%s and is_del=0"""
        a_tuple = CustomSQL(q=q,p=[request.user.email,]).fetchone()
        share_folder = a_tuple[0]
    except Exception as e:
        share_folder= 0
    t = {
            "print_record":print_record,
            "my_printer":my_printer,
            "my_friends":my_friends,
            "print_count":print_count,
            "printer_num":p_num,
            "used_num":used_num,
            "remain_days":remain_days,
            "ins_file":ins_file,
            "share_filder":share_folder,
            }
    return render(request,"user/index.html",t)

@login_required
def new_info(request):
    if request.method=="POST":
        update_data={}
        update_data['nick']=request.POST.get("nick")
        update_data['mobile']=request.POST.get("mobile")
        t={"status":0,"msg":"","nick":update_data['nick'],"mobile":update_data['mobile']}
        try:
            avatar_obj = KxUser.objects.filter(email=request.user.email).update(nick=update_data["nick"],mobile=update_data["mobile"])
            t['status']=1
            t['msg']="修改个人资料成功"
        except Exception, e:
            logger.debug(u"插入数据库失败！%s",e)
            t['msg']="修改个人资料失败"
    else:
        t={}
    return render(request,"user/info.html",t)

@login_required
def avatar(request):
    t={"avatar":request.user.avatar}
    if request.method=="POST":
        image = request.FILES.get("avatar",None)
        upload_info=avatar_edit(image)
        t["status"]=0
        t["msg"]=""
        print upload_info
        if upload_info[0]==0:
           t['msg']=upload_info[1]
        elif upload_info[0]==1:
            try:
                avatar_obj = KxUser.objects.filter(email=request.user.email).update(avatar=upload_info[1])
                t['status']=1
                t['msg']="修改头像成功"
                t['avatar']=upload_info[1]
                #todo 清除原有头像
            except Exception, e:
                logger.debug(u"更新用户头像失败！%s",e)
                t['msg']="修改个人资料失败"
        elif upload_info[0]==2:
             t['msg']="请上传头像"   
    return render(request,"user/avatar.html",t)

@login_required
@require_GET
def printer_auth(request):
    now = datetime.datetime.now()
    #operator = Operator.objects.filter(user=request.user.pk).filter(status__exact=1).filter(expire__gt=now).filter(operatorassistant__status__exact=1)
    operator = Operator.objects.filter(user=request.user.pk).filter(status__exact=1).filter(expire__gt=now)
    num = operator.values('printer_num','used_num')
    oa_user = operator.filter(operatorassistant__status__exact=1).values_list('operatorassistant__user__email')
    my_friends = KxUserFriend.objects.filter(user=request.user.email).values('friend')
    users = KxUser.objects.filter(email__in=my_friends)
    oa = []
    for i in oa_user:
        oa.append(i[0])
    if operator:
            
        t = {
                "users":users,
                "num":num[0],
                "oa":oa,
                }
        return render(request,"user/printer_auth.html",t)
    else:
        t = {
                "warning":u'没有浏览权限',
                "url":u'<a href="http://www.simplenect.cn/buy">请升级套餐</a>',
                }
        return render(request,"user/printer_auth.html",t)


@login_required()
@csrf_exempt
@require_POST
def do_auth(request):
    message = {}
    now = datetime.datetime.now()
    pid = request.POST.get("id","")
    uid = request.POST.get("uid","")
    flag = request.POST.get("flag","")
    logger.info("uid:%s,pid:%s",uid,pid)
    if pid and uid:
        op_obj = Operator.objects.filter(user_id =uid)
        if op_obj:
            op_id = op_obj.values('id')[0]['id']
            #name = op_obj.values('user__nick')[0]['user__nick']
            user_email = op_obj.values('user__email')[0]['user__email']
            used_num = op_obj.values()[0]['used_num']
            printer_num = op_obj.values()[0]['printer_num']
            op = OperatorAssistant.objects.filter(operator__user__id=uid).filter(operator__status__exact=1).filter(operator__expire__gt=now).filter(user_id=pid)
            my_friends = KxUserFriend.objects.filter(user=user_email).values_list('friend')
            users = KxUser.objects.filter(id=pid).values_list('email')
            if users and my_friends:
                for i in users:
                    if i in my_friends:
                        if flag == u'1':
                            if  used_num >=0 and used_num >= printer_num:
                                #打印机数大于已经使用的数量不允许授权
                                message['status']=1
                                message['info']=u"您的授权人数达到上限,请升级套餐！"
                                message['data']=0
                                return HttpResponse(json.dumps(message),content_type="application/json")
                            elif not op :
                                try:
                                    oa = OperatorAssistant.objects.create(operator_id=op_id,user_id=pid,created=now,status=1)
                                    oa.save()
                                    new = used_num+1
                                    op_obj.update(used_num=new)
                                    message['status']=1
                                    message['info']=u"添加授权成功!"
                                    message['data']=0
                                    return HttpResponse(json.dumps(message),content_type="application/json")
                                except Exception as e:
                                    message['status']=1
                                    message['info']=u"授权出现错误，请重试!"
                                    message['data']=0
                                    return HttpResponse(json.dumps(message),content_type="application/json")
                            elif used_num < printer_num and used_num >=0:
                                new = used_num+1
                                op_obj.update(used_num=new)
                                op.update(status=1)
                                message['status']=1
                                message['info']=u"授权成功！"
                                message['data']=0
                                return HttpResponse(json.dumps(message,ensure_ascii=False),content_type="application/json")
                            else:
                                message['status']=1
                                message['info']=u"授权失败！"
                                message['data']=0
                                return HttpResponse(json.dumps(message,ensure_ascii=False),content_type="application/json")
                        elif flag == u'0' and used_num > 0:
                            new = used_num-1
                            op_obj.update(used_num=new)
                            op.update(status=0)
                            message['status']=1
                            message['info']=u"取消授权成功！"
                            message['data']=0
                            return HttpResponse(json.dumps(message,ensure_ascii=False),content_type="application/json")
                        else:
                            message['status']=1
                            message['info']=u"取消授权失败！"
                            message['data']=0
                            return HttpResponse(json.dumps(message,ensure_ascii=False),content_type="application/json")
                    else:
                        message['status']=0
                        message['info']=u"授权失败!"
                        message['data']=0
                        return HttpResponse(json.dumps(message),content_type="application/json")
            else:
                message['status']=0
                message['info']=u"失败!"
                message['data']=0
                return HttpResponse(json.dumps(message),content_type="application/json")
        else:
            message['status']=0
            message['info']=u"失败!"
            message['data']=0
            return HttpResponse(json.dumps(message),content_type="application/json")

    else:
        message['status']=0
        message['info']=u"失败!"
        message['data']=0
        return HttpResponse(json.dumps(message),content_type="application/json")
    

@login_required()
@require_GET
def print_record(request):
    print_record = Spool.objects.filter(origin_email=request.user.email).order_by("-print_time")
    pages = print_record.aggregate(pages=Sum("page_num"))
    return render(request,"user/print_record.html",{"print_record":print_record,"pages":pages})

@login_required()
def my_printer(request):
    if request.method == "POST":
        email = request.POST.get('email','')
        if email:
            print_record = Spool.objects.filter(accept_email=request.user.email).filter(origin_email=email).order_by("-print_time")
            pages = print_record.aggregate(pages=Sum("page_num"))
            return render(request,"user/my_printer.html",{"print_record":print_record,"pages":pages})
        else:
            print_record = Spool.objects.filter(accept_email=request.user.email).order_by("-print_time")
            pages = print_record.aggregate(pages=Sum("page_num"))
            return render(request,"user/my_printer.html",{"print_record":print_record,"pages":pages})
    elif request.method == "GET":
        print_record = Spool.objects.filter(accept_email=request.user.email).order_by("-print_time")
        pages = print_record.aggregate(pages=Sum("page_num"))
        return render(request,"user/my_printer.html",{"print_record":print_record,"pages":pages})


@require_POST
def my_issue(request):
    """用户验证信息接口 flag=1 获取用户的验证问题，flag=2 设置用户的验证问题"""
    flag=request.POST.get("flag","0").strip()
    uid=request.POST.get("uid","").strip()
    json_data={}
    if flag=="1":
        myIssue=getUserAuthIssueByUser(uid)
        if myIssue:
            json_data['auth']=myIssue.is_auth
            json_data['issue']=myIssue.issue
        else: 
            json_data['auth']=-1
            json_data['issue']=""
    elif flag=="2":
        auth=0
        json_data['status']=0
        issue=request.POST.get("issue","").strip()
        try:
            auth=int(request.POST.get("auth"))
        except Exception,e:
            logger.error("auth 必须是数字0或1：%s",e)
            json_data['info']="param err01"
            return json_return(json_data)
        userCount=getUserCountByCondition({"uuid":uid})
        if userCount is None:
            json_data['info']="get user error"
            return json_return(json_data)
        if userCount==0:
            json_data['info']="no such user"
            return json_return(json_data)
        myIssue=getUserAuthIssueByUser(uid)
        if myIssue:
            result=updateUserAuthIssueByCondition({"user_id":uid},{"is_auth":auth,"issue":issue})
            if result:
                json_data['status']=1
                json_data['info']="update ok"
            else:
                json_data['info']="update err"
        else:
            userAuth=UserAuthIssue(user_id=uid,is_auth=auth,issue=issue)
            authId=insertUserAuthIssue(userAuth)
            if authId:
                json_data['status']=1
                json_data['info']="add ok"
            else:
                json_data['info']="add err"
    else:
        json_data['status']=0
        json_data['info']="param err02"
    return json_return(json_data)


def show_group_users(request):
    t={}
    return render(request,"user/printer_auth.html",t)
