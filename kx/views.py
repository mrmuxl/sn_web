#_*_coding:utf-8_*_
# Create your views here.

from django.http import Http404
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from kx.models import KxUser,KxMsgBoard
from django.contrib.auth import authenticate
from django.contrib import auth,messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
import uuid,os,datetime,json,logging
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from PIL import Image

logger = logging.getLogger(__name__)

def index(request):
    data={"title":u"首页"}
    time_tag  = ' 23:59:59'
    today = datetime.date.today()
    last_month =str(today-datetime.timedelta(days=30))
    left_create_time = last_month + time_tag
    #left_create_time = '2013-02-1 23:59:59'
    right_create_time = str(today) + time_tag
    #right_create_time = '2013-03-1 23:59:59'
    msg_count = KxMsgBoard.objects.filter(is_del__exact=0).count()
    data.update(msg_count=msg_count)
    msg_list = KxMsgBoard.objects.filter(reply_id__exact=0,is_del__exact=0,create_time__gte=left_create_time,create_time__lte=right_create_time).order_by("-create_time").values()[:5]
    data.update(msg_list=msg_list)
    #print "msg_list",msg_list
    reply_ids = []
    user_ids = []
    for i in msg_list:
        if i['id'] >0:
            reply_ids.append(i['id'])
        if i['user_id'] >0:
            user_ids.append(i['user_id'])
    if reply_ids:
        try:
            reply_list = KxMsgBoard.objects.filter(is_del__exact=0,reply_id__gt=0,reply_id__in=reply_ids).order_by("create_time").values('id','reply_id','msg')
        except:
            raise Http404
        reply_dict={}
        for r in reply_list:
            reply_dict[r["id"]] = r
        data.update(reply_list=reply_dict)
        #print "reply_list",reply_dict
    if user_ids:
        user_list = KxUser.objects.filter(id__in=user_ids).values('id','avatar')
        data.update(user_list=user_list)
        #print "user_list",user_list
    #print data
    return render(request,"index.html",data) 

def msg_board(request):
    data={"title":u"留言板"}
    time_tag  = ' 23:59:59'
    today = datetime.date.today()
    last_month =str(today-datetime.timedelta(days=30))
    #left_create_time = last_month + time_tag
    left_create_time = '2013-01-1 23:59:59'
    right_create_time = str(today) + time_tag
    #right_create_time = '2013-03-1 23:59:59'
    msg_list = KxMsgBoard.objects.filter(reply_id__exact=0,is_del__exact=0,create_time__gte=left_create_time,create_time__lte=right_create_time).order_by("-create_time").values()[:20]
    data.update(msg_list=msg_list)
    #print "msg_list",msg_list
    reply_ids = []
    user_ids = []
    for i in msg_list:
        if i['id'] >0:
            reply_ids.append(i['id'])
        if i['user_id'] >0:
            user_ids.append(i['user_id'])
    if reply_ids:
        try:
            reply_list = KxMsgBoard.objects.filter(is_del__exact=0,reply_id__gt=0,reply_id__in=reply_ids).order_by("create_time").values('id','reply_id','msg')
        except:
            raise Http404
        reply_dict={}
        for r in reply_list:
            reply_dict[r["id"]] = r
        data.update(reply_list=reply_dict)
        #print "reply_list",reply_dict
    if user_ids:
        user_list = KxUser.objects.filter(id__in=user_ids).values('id','avatar')
        #user_list=[{'id': 8361L, 'avatar':u'folder=User/2013/03/16,uid=810398361,ext=jpg,swidth=0,sheight=0,name=000.jpg,size=3745' }, {'id': 8371L, 'avatar':u'folder=User/2013/03/17,uid=810398371,ext=jpg,swidth=0,sheight=0,name=000.jpg,size=3745'},{'id': 9554L, 'avatar': u'folder=User/2013/02/19,uid=810399720,ext=jpg,swidth=0,sheight=0,name=000.jpg,size=3745'}]
        u_list=[]
        ul = []
        for u in user_list:
            if u['avatar']:
                ul.append([u"id",u['id']])
                for l in u['avatar'].split(','):
                    ul.append(l.split('='))
            user_dict=dict(ul)    
            if user_dict:
                u_list.append(user_dict)
            ul=[]
        data.update(user_list=u_list)
    return render(request,"msg_index.html",data) 

def add_msg(request):
    if request.method =="POST":
        msg = strip_tags(request.POST.get("msg").strip()).strip()
        ip = request.META.get('REMOTE_ADDR','')
        create_time = datetime.datetime.now()
        reply = request.POST.get("reply")
        if msg:
            if reply is not None:
                try:
                    reply_id = int(strip_tags(reply.strip()))
                except ValueError:
                    raise Http404
                if reply_id and reply_id > 0:
                    reply_find = KxMsgBoard.objects.filter(reply_id__exact=reply_id).values('id','reply_id')
                    for i in reply_find:
                        if i['reply_id'] and i['reply_id'] == reply_id:
                            pass
                        else:
                            return HttpResponse(u'您要回复的留言不存在！<A HREF="javascript:history.back()">返 回</A>')
            else:
                reply_id = 0
            if request.user.is_authenticated() and not request.user.is_anonymous():
                user_id = request.user.id
                user_nick = request.user.nick
                try:
                    reply_create = KxMsgBoard.objects.create(ip=ip,msg=msg,create_time=create_time,reply_id=reply_id,user_id=user_id,user_nick=user_nick)
                except:
                    raise Http404
                return HttpResponseRedirect(reverse("msg_show"))    
            else:
                try:
                    reply_create = KxMsgBoard.objects.create(ip=ip,msg=msg,create_time=create_time,reply_id=reply_id)
                except:
                    raise Http404
                return HttpResponseRedirect(reverse("msg_show"))    
        else:
            return HttpResponse(u'请填写留言内容！<A HREF="javascript:history.back()">返 回</A>')
    return HttpResponseRedirect(reverse("msg_show"))    

def register(request):
    '''注册视图'''
    return render_to_response("register.html",{},context_instance=RequestContext(request))
        
def check(request):
    if request.method =="POST":
        email = strip_tags(request.POST.get("email").strip())
        if not email:
            return HttpResponse(json.dumps({"data":0,"info":"","status":0}),content_type="application/json")
        else:
            count = KxUser.objects.filter(email=email).count()
            if count == 0:
                return HttpResponse(json.dumps({"data":1,"info":"OK","status":1}),content_type="application/json")
    return HttpResponse(json.dumps({"data":0,"info":"","status":0}),content_type="application/json")

 
def save(request):
    if request.method == "POST":
        email = strip_tags(request.POST.get("email").lower().strip())
        nick = strip_tags(request.POST.get("nick").strip())
        password = request.POST.get("password").strip()
        repassword = request.POST.get("repassword").strip()
        raw_email ="""请填写邮箱！<A HREF="javascript:history.back()">返 回</A>"""
        raw_nick ="""请填昵称！<A HREF="javascript:history.back()">返 回</A>"""
        raw_nick_length ="""昵称应为4-12个字符！<A HREF="javascript:history.back()">返 回</A>"""
        raw_password ="""请填写密码！<A HREF="javascript:history.back()">返 回</A>"""
        raw_repassword ="""两次密码填写不一致！<A HREF="javascript:history.back()">返 回</A>"""
        raw_has_email= """邮箱已存在！<A HREF="javascript:history.back()">返 回</A>"""
        if not email:
            return HttpResponse(raw_email)
        if not nick:
            return HttpResponse(raw_nick)
        if len(nick)<4 and len(nick)>12:
            return HttpResponse(raw_nick_length)
        if not password:
            return HttpResponse(raw_password)
        if password != repassword:
            return HttpResponse(raw_nick_length)
        count = KxUser.objects.filter(email=email).count()
        if count >0:
            return HttpResponse(raw_has_email)
        create_user=KxUser.objects.create_user(email=email,nick=nick,password=password,status=0)
        create_user.save()
        user = authenticate(username=email,password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
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

def logout(request):
    '''注销视图'''
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


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
            if ext in ('png','jpg','gif','bmp'):
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
                    return HttpResponseRedirect(reverse('info'))
                except Exception as e:
                    logger.debug(u"压缩图片失败！%s",e)
                    return HttpResponse("""上传文件失败请重新上传！<A HREF="javascript:history.back()">返 回</A>""")
            else:
                return HttpResponse("""不是支持的文件类型！<A HREF="javascript:history.back()">返 回</A>""")
        else:
            return HttpResponse("""请上传一张图片！<A HREF="javascript:history.back()">返 回</A>""")
    return HttpResponseRedirect(reverse('info'))

def post(request):
    pass
def chpasswd(request):
    pass
def tongji(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request,"tongji.html",{})
def login_tongji(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request,"login_tongji.html",{})

