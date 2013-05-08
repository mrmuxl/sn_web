#_*_coding:utf-8_*_

import logging
from django.http import Http404
from kx.models import KxPub
from django.views.decorators.http import (require_POST,require_GET)
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from forms import PublishAdd
from django.conf import settings

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
                ins = request.FILES['ins']
                patch = request.FILES['patch']

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
def del_pub(request):
    pass

def handle_uploaded_file(ins=None,patch=None):
    path_root = settings.PUBLISH_UPLOAD

    try:
        if not os.path.isdir(path_folder):
            os.makedirs(path_folder)
        with open(path_upload,'wb') as fd:
            for chunk in image.chunks():
                fd.write(chunk)
    except Exception as e:
        logger.debug(u"文件上传失败！%s",e)

