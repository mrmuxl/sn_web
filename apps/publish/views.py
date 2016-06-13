#_*_coding:utf-8_*_

import datetime,logging,json,os
from django.conf import settings
from django.http import Http404
from apps.kx.models import KxPub
from django.views.decorators.http import (require_POST,require_GET)
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from forms import PublishAdd
from utils import handle_uploaded_file,update_download_link

logger = logging.getLogger(__name__)

@require_GET
def publish_index(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('login'))
    else:
        #try:
        #    p = int(request.GET.get('p','1'))
        #except ValueError:
        #    p = 1
        #try:
        #    pub_count = KxPub.objects.all().count()
        #    logger.info("%s",pub_count)
        #except Exception as e:
        #    pub_count = 0
        #    logger.debug("%s",e)
        try:
            pub_list = KxPub.objects.order_by('-id').values()
            logger.info("%s",pub_list)
        except Exception as e:
            pub_list = []
            logger.debug("%s",e)
        t_var = {
                    'pub_list':pub_list,
                }
        return render(request,"publish/index.html",t_var)

def publish_add(request):
    now = datetime.datetime.now()
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('login'))
    else:
        if request.method == "POST":
            form = PublishAdd(request.POST,request.FILES,auto_id=False) 
            if form.is_valid():
                pub_id =form.cleaned_data['id']
                ver = form.cleaned_data['ver']
                desc = form.cleaned_data['desc']
                try:
                    ins = request.FILES['ins']
                    handle_uploaded_file(ver=ver,ins=ins)
                except KeyError as e:
                    logger.debug("ins参数不存在%s",e)
                except OSError as e:
                    logger.debug("目录创建错误%s",e)
                    message ="""目录创建错误,没有创建目录的权限！<A HREF="javascript:history.back()">返 回</A>"""
                    return HttpResponse(message)
                except IOError as e:
                    logger.debug("publish_add,安装包上传失败！%s",e)
                    message ="""安装包上传失败！<A HREF="javascript:history.back()">返 回</A>"""
                    return HttpResponse(message)
                try:
                    patch = request.FILES['patch']
                    handle_uploaded_file(ver=ver,patch=patch)
                except KeyError as e:
                    logger.debug("%s",e)
                except OSError as e:
                    logger.debug("目录创建错误%s",e)
                    message ="""目录创建失败,不允许创建目录！<A HREF="javascript:history.back()">返 回</A>"""
                    return HttpResponse(message)
                except IOError as e:
                    logger.debug("publish_add,patch包上传失败！%s",e)
                    message ="""patch上传失败！<A HREF="javascript:history.back()">返 回</A>"""
                    return HttpResponse(message)
                try:
                    ins_file = "Qianmo_" + ver.upper() + ".zip"
                    patch_file = ver + "/Patch.zip"
                    if pub_id:
                        pub_edit = KxPub.objects.filter(id=pub_id).update(pub_desc=desc,install_file=ins_file,patch_file=patch_file,create_time=now,is_tongji=1)
                    else:
                        pub_add = KxPub.objects.create(ver=ver,pub_desc=desc,install_file=ins_file,patch_file=patch_file,create_time=now,is_tongji=1)
                except Exception as e:
                    logger.debug("%s",e)
                return HttpResponseRedirect(reverse('publish_index'))
            t_var ={'form':form}
            return render(request,"publish/add.html",t_var)
        elif request.method == "GET":
            pub_id = request.GET.get('id','')
            if pub_id:
                pub_id = int(pub_id)
                try:
                    pub_obj = KxPub.objects.get(id=pub_id) 
                    form_init = {
                                    'id':pub_obj.id,
                                    'ver':pub_obj.ver,
                                    'desc':pub_obj.pub_desc,
                                  }
                    form = PublishAdd(initial=form_init,auto_id=False)
                    t_var ={'form':form}
                    return render(request,"publish/add.html",t_var)
                except Exception as e:
                    logger.debug("%s",e)
            else:
                try:
                    ver_obj = KxPub.objects.order_by('-id')[0:1].get()
                    current_ver = ver_obj.ver.split('.')
                    prefix_ver = current_ver[0:-1]
                    suffix_ver = unicode(int(current_ver[-1:][0])+1)
                    prefix_ver.append(suffix_ver)
                    form_data = '.'.join(prefix_ver)
                    form_init = {'ver':form_data}
                    form = PublishAdd(initial=form_init,auto_id=False) 
                    t_var ={'form':form}
                    return render(request,"publish/add.html",t_var)
                except Exception as e:
                    form = PublishAdd(auto_id=False) 
                    t_var ={'form':form}
                    return render(request,"publish/add.html",t_var)

def publish_edit(request):
    return render(request,"publish/edit.html",{})

@require_POST
def do_pub(request):
    now = datetime.datetime.now()
    message={}
    if request.user.is_superuser:
        pub_id = request.POST.get("id","")
        if pub_id:
            pub_id = int(pub_id)
            try:
                pub_obj = KxPub.objects.get(id=pub_id)
                if not pub_obj.pub_time:
                    try:
                        pub_update = KxPub.objects.filter(id=pub_id).update(pub_time=now)
                        try:
                            install_file = pub_obj.install_file
                            update_download_link(install_file)
                        except Exception as e:
                            logger.debug("%s",e)
                            message['status']=0
                            message['info']=u"更新发布链接失败！"
                            message['data']=0
                            return HttpResponse(json.dumps(message),content_type="application/json")
                        message['status']=1
                        message['info']=u"发布成功！"
                        message['data']=str(now)[:19]
                        return HttpResponse(json.dumps(message),content_type="application/json")
                    except Exception as e:
                        logger.debug("%s",e)
                        message['status']=0
                        message['info']=u"发布失败请重试！"
                        message['data']=0
                        return HttpResponse(json.dumps(message),content_type="application/json")
                else:
                    message['status']=0
                    message['info']=u'当前发布已正式发布！'
                    message['data']=0
                    return HttpResponse(json.dumps(message),content_type="application/json")
            except Exception as e:
                logger.debug("%s",e)
        else:
            message['status']=0
            message['info']=u'当前发布不存在！'
            message['data']=0
            return HttpResponse(json.dumps(message),content_type="application/json")
    else:
        message['status']=0
        message['info']="deny!"
        message['data']=0
        return HttpResponse(json.dumps(message),content_type="application/json")



@require_POST
def del_pub(request):
    message={}
    if request.user.is_superuser:
        pub_id = request.POST.get("id","")
        if pub_id:
            pub_id = int(pub_id)
            try:
                pub_obj = KxPub.objects.get(id=pub_id)
                if not pub_obj.pub_time:
                    try:
                        pub_del = KxPub.objects.filter(id=pub_id).delete()
                        message['status']=1
                        message['info']=u"删除发布成功！"
                        message['data']=1
                        return HttpResponse(json.dumps(message),content_type="application/json")
                    except Exception as e:
                        logger.debug("%s",e)
                        message['status']=0
                        message['info']=u"删除发布不存在！"
                        message['data']=0
                        return HttpResponse(json.dumps(message),content_type="application/json")
                else:
                    message['status']=0
                    message['info']=u'已正式发布的不允许删除！'
                    message['data']=0
                    return HttpResponse(json.dumps(message),content_type="application/json")
            except Exception as e:
                logger.debug("%s",e)
        else:
            message['status']=0
            message['info']=u'要删除的发布不存在！'
            message['data']=0
            return HttpResponse(json.dumps(message),content_type="application/json")

    else:
        message['status']=0
        message['info']="deny!"
        message['data']=0
        return HttpResponse(json.dumps(message),content_type="application/json")