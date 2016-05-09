#_*_coding:utf-8_*_

import logging
from django.http import Http404
from kx.models import KxPub
from django.views.decorators.http import (require_POST,require_GET)
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from forms import PublishAdd
from utils import handle_uploaded_file

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
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('login'))
    else:
        if request.method == "POST":
            form = PublishAdd(request.POST,request.FILES,auto_id=False) 
            if form.is_valid():
                ver = form.cleaned_data['ver']
                desc = form.cleaned_data['desc']
                try:
                    ins = request.FILES['ins']
                    handle_uploaded_file(ver=ver,ins=ins)
                except KeyError as e:
                    logger.debug("ins参数不存在%s",e)
                except OSError as e:
                    logger.debug("目录创建错误%s",e)
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
                except IOError as e:
                    logger.debug("publish_add,patch包上传失败！%s",e)
                    message ="""patch上传失败！<A HREF="javascript:history.back()">返 回</A>"""
                    return HttpResponse(message)
                return HttpResponseRedirect(reverse('publish_index'))
            t_var ={'form':form}
            return render(request,"publish/add.html",t_var)

        else:
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

def publish_edit(request):
    return render(request,"publish/edit.html",{})

def do_pub(request):
    pass


@require_POST
def del_pub(request):
    message={}
    if request.user.is_superuser:
        msg_id = request.POST.get("id","")
        if msg_id:
            msg_id = int(msg_id)
            try:
                msg_obj = KxMsgBoard.objects.filter(id=msg_id).delete()
                message['status']=1
                message['info']="ok"
                message['data']=1
                return HttpResponse(json.dumps(message),content_type="application/json")
            except Exception as e:
                logger.debug("%s",e)
                message['status']=0
                message['info']="false"
                message['data']=0
                return HttpResponse(json.dumps(message),content_type="application/json")
    else:
        message['status']=0
        message['info']="deny!权限不够"
        message['data']=0
        return HttpResponse(json.dumps(message),content_type="application/json")
