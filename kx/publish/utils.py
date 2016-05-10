#_*_coding:utf-8_*_

import logging,os
from django.conf import settings

logger = logging.getLogger(__name__)

def handle_uploaded_file(ver=None,ins=None,patch=None):
    path_root = settings.PUBLISH_UPLOAD
    if ins is not None:
        path_folder=path_root + "/Install/"
        path_upload = path_folder + "Qianmo_" + ver + ".zip"
        do_upload(path_folder,path_upload,ins)
    if patch is not None:
        path_folder=path_root + "/Install/" + ver + "/"
        path_upload = path_folder + "Patch.zip"
        do_upload(path_folder,path_upload,patch)

def do_upload(path_folder,path_upload,upload_file):
    try:
        if not os.path.isdir(path_folder):
            os.makedirs(path_folder)
        with open(path_upload,'wb') as fd:
            for chunk in upload_file.chunks():
                fd.write(chunk)
    except OSError as e:
        logger.debug(u"目录创建失败！%s",e)
        raise 
    except IOError as e:
        logger.debug(u"文件上传失败！%s",e)
        raise 

def update_download_link(install_file):
    print install_file
    download_html = u'<span> <a href="' + settings.DOMAIN + u'/Install/' + install_file + u'" target="_blank" title="下载">'
    download_html += u'<img src="{{ STATIC_URL }}images/download_btn2.png" class="mypng" /></a></span>'
    download_html=download_html.encode('utf8')
    fname = os.path.join(settings.ROOT_DIR,'templates' + settings.THEME)
    fname += "index_download.html"
    try:
        with open(fname,'w') as fd:
            fd.write(download_html)
    except EnvironmentError as e:
        logger.debug(u"写跟新发布文件错误！%s",e)
        raise 
