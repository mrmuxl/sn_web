#_*_coding:utf-8_*_

from django.conf import settings
import uuid,os,json,logging,time,shutil
from datetime import datetime,date
from PIL import Image
logger = logging.getLogger(__name__)
def invite_register(from_nick,invite_content,reg_url):
    msg = u'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
              <html xmlns="http://www.w3.org/1999/xhtml">
              <head></head><body><div class="main" style="width:100%;color:#000000;background-color:f8f8f8;font:12px/1.5 Microsoft Yahei,宋体,arial,\5b8b\4f53;">
              <div class="content" style="width:600px;margin:0 auto;font-size:16px;"> <div class="title" style="width:600px;height:64px;line-height:64px;">'''
    msg += u'''<span style="font-size:18px;color:#0e5bbf;">''' + from_nick  + u'''</span>&nbsp;邀请您一起使用办公协同软件：SimpleNect </div>'''
    msg += u'''<div class="invate_msg" style="color:#838383;line-height:45px;word-wrap: break-word;"> &nbsp;&nbsp;&nbsp;&nbsp;“''' + invite_content + u'''” </div>'''
    msg += u'''<div class="download_area" style="height:64px;width:222px;margin-left:203px;margin-top:18px;">'''
    msg += u'''<a href="'''  + settings.DOMAIN  + u'''"> <img src="'''  + settings.STATIC_URL  + u'''images/email_download.jpg" style="border:none;"/></a></div>'''
    msg += u'''<div class="fun_area" style="width:548px;margin-left:30px;margin-top:48px;"><div class="fun_area_title" style="">SimpleNect能够：</div>'''
    msg += u'''<div class="fun_img"><img src="''' + settings.STATIC_URL + u'''images/email_fun.jpg" /> </div>'''
    msg += u'''<div class="fun_area_text" style="margin-top:20px;line-height:35px;word-wrap: break-word;color:#838383;"> SimpleNect大大
               <span style="font-size:17px;color:#000000;">简化</span>了共享文件和打印机的操作，更把共享的范围从局域 网扩展到整个
               <span style="font-size:17px;color:#000000;">互联网</span>，也就是说A用户在上海，B用户在北京，两人仍然可以通过SimpleNect
               <span style="font-size:17px;color:#000000;">共享</span>自己电脑里的文件或打印机</div>
               <div class="fun_area_link" style="margin:10px 0 10px 0;height:26px;line-height:26px;text-align:right;">'''
    msg += u'''<a href="''' + reg_url + u'''" style="color:#0e5bbf;text-decoration:underline;">访问SimpleNect网站</a>'''
    msg += u'''</div></div><div class="content_foot" style="height:50px;"></div></div></div></body></html>''' 
    return msg

def invite_tip(from_nick,invite_content,site_url):
    msg = u'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
              <html xmlns="http://www.w3.org/1999/xhtml">
              <head></head><body><div class="main" style="width:100%;color:#000000;background-color:f8f8f8;font:12px/1.5 Microsoft Yahei,宋体,arial;">
              <div class="content" style="width:600px;margin:0 auto;font-size:16px;">'''
    msg += u'''<div class="title" style="width:600px;height:50px;line-height:50px;"><span style="font-size:18px;color:#0e5bbf;">'''  + from_nick 
    msg += u'''</span>&nbsp;''' + invite_content + u'''</div>'''
    msg += u'''<div class="fun_area" style="width:548px;margin-left:30px;margin-top:48px;">
               <div class="fun_area_link" style="margin:10px 0 10px 0;height:26px;line-height:26px;text-align:right;">'''
    msg += u'''<a href="''' + site_url + u'''" style="color:#0e5bbf;text-decoration:underline;">访问SimpleNect网站</a>
               </div></div><div class="content_foot" style="height:50px;"></div></div></div></body></html>'''
    return msg

def avatar_edit(image):
    if image:
        datePath =date.strftime(date.today(),"%Y/%m/%d")
        uid = uuid.UUID.time_low.fget(uuid.uuid4())
        folder = "User/"+str(datePath)
        ext = str(image.content_type).split("/")[-1:][0]
        if ext in ('png','jpeg','gif','bmp'):
            file_name = image.name.encode('utf-8')
            file_size = str(image.size)
            file_uid = str(uid) 
            path_root = settings.MEDIA_ROOT
            path_folder = path_root + folder
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
                    return 0,"上传图片失败！"
                size_50 = (50,50)
                size_60 = (60,60)
                image = Image.open(path_upload)
                if image.format == 'GIF':
                    image = image.convert('RGB')
                image.save(path_save,format="jpeg",quality=100)
                image.resize(size_50,Image.ANTIALIAS).save(save_50,format="jpeg",quality=95)
                image.resize(size_60,Image.ANTIALIAS).save(save_60,format="jpeg",quality=95)
                if os.path.exists(save_60) and os.path.exists(path_save):
                    shutil.copy(save_60,path_save)
                return 1,avatar_info
            except Exception as e:
                logger.debug(u"压缩图片失败！%s",e)
                return 0,"""上传文件失败请重新上传！"""
        else:
            return 0,"""不是支持的文件类型！"""
    else:
        return 2,"""未上传图片"""