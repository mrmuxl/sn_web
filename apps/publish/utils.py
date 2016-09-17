#_*_coding:utf-8_*_

import logging,os
from django.conf import settings
from hashlib import md5
#from ordereddict import OrderedDict

logger = logging.getLogger(__name__)

def handle_uploaded_file(ver=None,ins=None,patch=None):
    path_root = settings.PUBLISH_UPLOAD
    if ins is not None:
        path_folder=path_root + "/Install/"
        path_upload = path_folder + "SimpleNect_" + ver.upper() + ".zip"
        install_md5 = do_upload(path_folder,path_upload,ins)
        if install_md5:
            return install_md5 
    if patch is not None:
        path_folder=path_root + "/Install/" + ver + "/"
        path_upload = path_folder + "Patch.zip"
        patch_md5 = do_upload(path_folder,path_upload,patch)
        if patch_md5:
            return patch_md5 

def do_upload(path_folder,path_upload,upload_file):
    try:
        if not os.path.isdir(path_folder):
            os.makedirs(path_folder)
        with open(path_upload,'wb') as fd:
            for chunk in upload_file.chunks():
                fd.write(chunk)
        with open(path_upload,'rb') as fd:
            file_md5 = md5(fd.read()).hexdigest()
        return file_md5
    except OSError as e:
        logger.debug(u"目录创建失败！%s",e)
        raise 
    except IOError as e:
        logger.debug(u"文件上传失败！%s",e)
        raise 

def update_download_link(install_file):
    download_html = u'<span> <a href="' + settings.DOWNLOAD + u'/Install/' + install_file + u'" target="_blank" title="下载">'
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

def publish_message(publish_info):
    message = {}
    if publish_info.patch_md5:
        patch_md5 = publish_info.patch_md5.upper()
        publish_info.patch_md5 = publish_info.patch_md5.upper()
    if publish_info.install_md5:
        publish_info.install_md5 = publish_info.install_md5.upper()
    ver_list = publish_info.ver.split('.')
    ver_dict={"Major":int(ver_list[0].strip('VvSs')),"Minor": int(ver_list[1]),"Build":int(ver_list[2]),"Revision":int(ver_list[3]),"MajorRevision":0,"MinorRevision": 0}
    standAloneVersion = []
    files = []
    file_patch = {"fileRelativePath":"Patch.zip","url":settings.DOWNLOAD+'/Install/'+publish_info.patch_file,"MD5":publish_info.patch_md5}
    file_ins = {"fileRelativePath":publish_info.install_file,"url":settings.DOWNLOAD+'/Install/'+publish_info.install_file,"MD5":publish_info.install_md5}
    files.append(file_patch)
    files.append(file_ins)
    stand_dict = {}
    stand_dict.update(ver=ver_dict)
    stand_dict.update(files=files)
    stand_dict.update(pubTime=str(publish_info.pub_time))
    stand_dict.update(URL=settings.DOWNLOAD)
    stand_dict.update(installFile="Patch.zip")
    stand_dict.update(installArgs=["/VERYSILENT",])
    standAloneVersion.append(stand_dict)
    message.update(standAloneVersion=standAloneVersion)
    message.update(netWorkVersion=[])
    if settings.DEBUG:
        from pprint import pprint 
        pprint(message)
    return message
