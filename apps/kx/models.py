#_*_coding:utf-8_*_
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin)
from apps.kx.kxmanager import KxUserManager
from django.conf import settings

class GroupGrade(models.Model):
    grade      = models.IntegerField(null = True, blank = True)
    begin_time = models.IntegerField(null = True, blank = True)
    end_time   = models.IntegerField(null = True, blank = True)
    class Meta:
        db_table = 'group_grade'

class KxActTongji(models.Model):
    id          = models.AutoField(default = None,primary_key = True)
    tongji_day  = models.DateField(default = None,unique = True)
    on_num      = models.IntegerField(default = 0)
    act_num     = models.IntegerField(default = 0)
    un_num      = models.IntegerField(default = 0)
    vc_val      = models.DecimalField(default = 0.00,max_digits  = 2, decimal_places = 2)
    trans0      = models.IntegerField(default = 0)
    trans1      = models.IntegerField(default = 0)
    trans2      = models.IntegerField(default = 0)
    trans3      = models.IntegerField(default = 0)
    print0      = models.IntegerField(default = 0)
    print1      = models.IntegerField(default = 0)
    print2      = models.IntegerField(default = 0)
    print3      = models.IntegerField(default = 0)
    chat0       = models.IntegerField(default = 0)
    chat1       = models.IntegerField(default = 0)
    chat2       = models.IntegerField(default = 0)
    chat3       = models.IntegerField(default = 0)
    friend0     = models.IntegerField(default = 0)
    friend1     = models.IntegerField(default = 0)
    friend2     = models.IntegerField(default = 0)
    friend3     = models.IntegerField(default = 0)
    invite0     = models.IntegerField(default = 0)
    invite1     = models.IntegerField(default = 0)
    invite2     = models.IntegerField(default = 0)
    invite3     = models.IntegerField(default = 0)
    invite4     = models.IntegerField(default = 0)
    friend_all0 = models.IntegerField(default = 0)
    friend_all1 = models.IntegerField(default = 0)
    friend_all2 = models.IntegerField(default = 0)
    friend_all3 = models.IntegerField(default = 0)
    class Meta:
        db_table = 'kx_act_tongji'

class KxAlipayOrder(models.Model):
    order_id       = models.CharField(max_length = 14L, primary_key = True)
    title          = models.CharField(max_length = 200L)
    pay_money      = models.DecimalField(max_digits = 10, decimal_places = 2)
    qianmo_dot     = models.IntegerField()
    add_qianmo_dot = models.IntegerField()
    user_id        = models.CharField(max_length=32L)
    trade_no       = models.CharField(max_length = 16L, blank = True)
    pay_status     = models.IntegerField()
    create_time    = models.DateTimeField()
    finish_time    = models.DateTimeField(null = True, blank = True)
    class Meta:
        db_table = 'kx_alipay_order'

class KxCscRecord(models.Model):
    id             = models.AutoField(primary_key = True)
    email          = models.CharField(max_length = 50L, null = True, blank = True)
    mac            = models.CharField(max_length = 100L,null = True, blank = True)
    called_email   = models.CharField(max_length = 50L, null = True, blank = True)
    called_mac     = models.CharField(max_length = 100L,null = True, blank = True)
    start_time     = models.DateTimeField(null = True, blank = True)
    end_time       = models.DateTimeField(null = True, blank = True)
    transferd_size = models.BigIntegerField(default = 0,null = True, blank = True)
    status         = models.IntegerField(default    = 0,null = True, blank = True)
    class Meta:
        db_table = 'kx_csc_record'

class KxEmailInvate(models.Model):
    id             = models.IntegerField(primary_key = True)
    user_id        = models.CharField(max_length=32L)
    user_name      = models.CharField(max_length = 20L)
    invate_email   = models.CharField(max_length = 50L)
    invate_name    = models.CharField(max_length = 20L)
    group_id       = models.IntegerField()
    group_name     = models.CharField(max_length = 50L)
    invate_code    = models.CharField(max_length = 50L, unique = True)
    qianmo_dot     = models.IntegerField()
    create_time    = models.DateTimeField()
    status         = models.IntegerField()
    register_email = models.CharField(max_length = 50L, blank = True)
    class Meta:
        db_table = 'kx_email_invate'

class KxEnt(models.Model):
    id                         = models.IntegerField(primary_key = True)
    ent_name                   = models.CharField(max_length = 40L)
    ent_country                = models.CharField(max_length = 15L, blank = True)
    ent_province               = models.CharField(max_length = 15L, blank = True)
    ent_city                   = models.CharField(max_length = 15L, blank = True)
    ent_address                = models.CharField(max_length = 70L, blank = True)
    ent_zipcode                = models.CharField(max_length = 7L,  blank = True)
    ent_contact1_nick          = models.CharField(max_length = 10L, blank = True)
    ent_contact1_tel           = models.CharField(max_length = 40L, blank = True)
    ent_contact1_phone         = models.CharField(max_length = 40L, blank = True)
    ent_contact2_nick          = models.CharField(max_length = 10L, blank = True)
    ent_contact2_tel           = models.CharField(max_length = 40L, blank = True)
    ent_contact2_phone         = models.CharField(max_length = 40L, blank = True)
    ent_reg_date               = models.DateTimeField()
    ent_status                 = models.IntegerField()
    ent_setup_indexmaxfilesize = models.IntegerField(db_column ='ent_setup_indexMaxFileSize') # Field name made lowercase.
    ent_user_num               = models.IntegerField()
    ent_master_id              = models.CharField(max_length=32L)
    create_time                = models.DateTimeField()
    update_time                = models.DateTimeField()
    version                    = models.IntegerField()
    class Meta:
        db_table = 'kx_ent'

class KxEntUser(models.Model):
    id          = models.IntegerField(primary_key = True)
    user_id     = models.CharField(max_length=32L)
    ent_id      = models.IntegerField()
    status      = models.IntegerField()
    update_time = models.DateTimeField()
    updater_id  = models.CharField(max_length=32L)
    class Meta:
        db_table = 'kx_ent_user'

class KxGroup(models.Model):
    groupid     = models.IntegerField(primary_key = True)
    groupname   = models.CharField(max_length = 50L)
    founder     = models.CharField(max_length = 50L)
    eff         = models.IntegerField()
    eff_date    = models.DateField()
    create_date = models.DateField()
    mem_nums    = models.IntegerField()
    max_members = models.IntegerField(null = True, blank = True)
    grade       = models.IntegerField()
    class Meta:
        db_table = 'kx_group'

class KxGroupmembers(models.Model):
    groupid   = models.IntegerField()
    email     = models.CharField(max_length = 50L)
    join_time = models.DateField()
    indentity = models.IntegerField()
    class Meta:
        db_table = 'kx_groupmembers'

class KxInvateRecord(models.Model):
    id          = models.IntegerField(primary_key = True)
    user_id     = models.CharField(max_length=32L)
    invate_id   = models.CharField(max_length=32L)
    qianmo_dot  = models.IntegerField()
    create_time = models.DateTimeField()
    class Meta:
        db_table = 'kx_invate_record'

class KxLanDay(models.Model):
    id         = models.IntegerField(primary_key = True)
    tongji_day = models.DateField(unique         = True)
    lan_num    = models.IntegerField()
    pc1        = models.IntegerField()
    pc2        = models.IntegerField()
    pc3        = models.IntegerField()
    pc4        = models.IntegerField()
    pc5        = models.IntegerField()
    pc6        = models.IntegerField()
    pc7        = models.IntegerField()
    qm1        = models.IntegerField()
    qm2        = models.IntegerField()
    qm3        = models.IntegerField()
    qm4        = models.IntegerField()
    qm5        = models.IntegerField()
    qm6        = models.IntegerField()
    qm7        = models.IntegerField()
    class Meta:
        db_table = 'kx_lan_day'

class KxLanTongji(models.Model):
    id = models.IntegerField(primary_key=True)
    ip = models.CharField(max_length=15L)
    tongji_day = models.DateField()
    pc_num = models.IntegerField()
    qm_num = models.IntegerField()
    class Meta:
        db_table = 'kx_lan_tongji'

class KxLoginRecord(models.Model):
    id = models.IntegerField(primary_key=True)
    login_day = models.DateField(unique=True)
    login_num = models.IntegerField()
    class Meta:
        db_table = 'kx_login_record'

class KxMailingAddfriend(models.Model):
    id               = models.IntegerField(primary_key = True)
    user             = models.CharField(max_length = 50L)
    friend           = models.CharField(max_length = 50L)
    invite_msg       = models.CharField(max_length = 200L)
    create_time      = models.DateTimeField()
    is_sendemail     = models.IntegerField()
    send_who         = models.IntegerField()
    send_reason_type = models.IntegerField()
    invite_content   = models.CharField(max_length = 200L, blank = True)
    is_del           = models.IntegerField()
    class Meta:
        db_table = 'kx_mailing_addfriend'

class KxMsgBoard(models.Model):
    id          = models.AutoField(primary_key = True)
    ip          = models.CharField(max_length = 15L,verbose_name=u'留言用户ip')
    msg         = models.CharField(max_length = 500L)
    create_time = models.DateTimeField(db_index=True,verbose_name=u'留言时间')
    reply_id    = models.IntegerField(db_index=True,default=0,verbose_name=u'要回复的留言ID，0表示新的留言')
    is_del      = models.BooleanField(default=False,verbose_name=u'是否删除，0=未删除，1=删除')
    user_id     = models.CharField(max_length=32L,default=0)
    user_nick   = models.CharField(max_length = 50L,default='--')
    class Meta:
        db_table = 'kx_msg_board'
    def __unicode__(self):
        return self.msg

class KxOrg(models.Model):
    id          = models.IntegerField(primary_key = True)
    name        = models.CharField(max_length = 20L)
    parent_id   = models.IntegerField()
    ent_id      = models.IntegerField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    updater_id  = models.CharField(max_length=32L)
    class Meta:
        db_table = 'kx_org'

class KxOrgSelf(models.Model):
    id             = models.IntegerField(primary_key = True)
    user_id        = models.CharField(max_length=32L)
    target_user_id = models.CharField(max_length=32L)
    ent_id         = models.IntegerField()
    create_time    = models.DateTimeField()
    update_time    = models.DateTimeField()
    updater_id     = models.CharField(max_length=32L)
    class Meta:
        db_table = 'kx_org_self'

class KxPub(models.Model):
    id           = models.IntegerField(primary_key = True)
    ver          = models.CharField(max_length = 30L, unique = True)
    pub_desc     = models.CharField(max_length = 600L)
    install_file = models.CharField(max_length = 100L, blank = True)
    patch_file   = models.CharField(max_length = 100L, blank = True)
    create_time  = models.DateTimeField()
    pub_time     = models.DateTimeField(null = True, blank = True)
    is_tongji    = models.IntegerField()
    class Meta:
        db_table = 'kx_pub'

class KxPubRecord(models.Model):
    id          = models.IntegerField(primary_key = True)
    email       = models.CharField(max_length     = 50L)
    tongji_time = models.DateTimeField()
    obj         = models.IntegerField()
    obj_val     = models.IntegerField()
    class Meta:
        db_table = 'kx_pub_record'

class KxPubTongji(models.Model):
    id      = models.IntegerField(primary_key = True)
    pub_id  = models.IntegerField(unique      = True)
    reg_num = models.IntegerField()
    act_num = models.IntegerField()
    un_num  = models.IntegerField()
    vc_val  = models.DecimalField(max_digits  = 4, decimal_places = 2)
    trans0  = models.IntegerField()
    trans1  = models.IntegerField()
    trans2  = models.IntegerField()
    trans3  = models.IntegerField()
    print0  = models.IntegerField()
    print1  = models.IntegerField()
    print2  = models.IntegerField()
    print3  = models.IntegerField()
    chat0   = models.IntegerField()
    chat1   = models.IntegerField()
    chat2   = models.IntegerField()
    chat3   = models.IntegerField()
    friend0 = models.IntegerField()
    friend1 = models.IntegerField()
    friend2 = models.IntegerField()
    friend3 = models.IntegerField()
    invite0 = models.IntegerField()
    invite1 = models.IntegerField()
    invite2 = models.IntegerField()
    invite3 = models.IntegerField()
    invite4 = models.IntegerField()
    class Meta:
        db_table = 'kx_pub_tongji'

class KxSoftBug(models.Model):
    id               = models.IntegerField(primary_key = True)
    client_identifie = models.CharField(max_length     = 32L)
    version          = models.CharField(max_length     = 10L)
    upload_time      = models.DateTimeField()
    os               = models.CharField(max_length     = 50L)
    auto_start       = models.IntegerField()
    lan_num          = models.IntegerField()
    u_email          = models.CharField(max_length     = 50L, blank = True)
    class Meta:
        db_table = 'kx_soft_bug'

class KxSoftRecord(models.Model):
    id               = models.AutoField(primary_key = True)
    client_identifie = models.CharField(db_index=True,max_length = 32L)
    version          = models.CharField(db_index=True,max_length = 10L)
    login_time       = models.DateTimeField()
    is_new           = models.BooleanField(default=False)
    is_uninstall     = models.BooleanField(default=False)
    class Meta:
        db_table = 'kx_soft_record'

class KxSoftUtime(models.Model):
    id               = models.IntegerField(primary_key = True)
    client_identifie = models.CharField(max_length = 32L)
    tongji_day       = models.DateField()
    utime            = models.IntegerField()
    create_time      = models.DateTimeField()
    class Meta:
        db_table     = 'kx_soft_utime'

class KxSystemInfo(models.Model):
    info_name = models.CharField(max_length=20L, primary_key=True)
    value = models.IntegerField()
    class Meta:
        db_table = 'kx_system_info'

class KxTongjiRecord(models.Model):
    id            = models.AutoField(primary_key = True)
    tongji_day    = models.DateField(unique = True)
    new_num       = models.IntegerField(default=0)
    un_num        = models.IntegerField(default=0)
    seven_new_num = models.IntegerField(default=0)
    seven_un_num  = models.IntegerField(default=0)
    last_mon_num  = models.IntegerField(default=0)
    cur_mon_num   = models.IntegerField(default=0)
    no_login_num  = models.IntegerField(default=0)
    all_num       = models.IntegerField(default=0)
    class Meta:
        db_table = 'kx_tongji_record'

STATUS_CHOICES = (
    (0, u'未激活'),
    (1, u'正常'),
    (2, u'封禁'),
)
class KxUser(AbstractBaseUser,PermissionsMixin):
    id                  = models.AutoField(primary_key = True)
    uuid                = models.CharField(db_index=True,max_length=32L)
    email               = models.EmailField(verbose_name=u'邮件地址', max_length=50, unique=True)
    nick                = models.CharField(u'用户昵称',max_length  = 20L)
    status              = models.IntegerField(u'用户状态',default = 0,choices=STATUS_CHOICES,help_text=u'0=未激活，1=正常，2=封禁')
    create_time         = models.DateTimeField(verbose_name=u'注册时间')
    update_time         = models.DateTimeField()
    avatar              = models.CharField(max_length = 200L, null = True,blank = True)
    last_ip             = models.CharField(max_length = 50L,  null = True,blank = True)
    mobile              = models.CharField(max_length = 20L,  null = True,blank = True)
    department          = models.CharField(max_length = 100L,  null = True,blank = True)
    login_status        = models.IntegerField(default = False,null = False)
    qianmo_dot          = models.IntegerField(u'现有阡陌点',default = 0,null = False)
    con_qianmo_dot      = models.IntegerField(u'累计消费阡陌点',default = 0)
    invate_init         = models.IntegerField(u'登陆状态',default = False,help_text=u'0 = 未登录,1 = 邀请用户登录并初始化成功，2 = 非邀请用')
    login_counts        = models.IntegerField(default = 0)
    create_group_counts = models.IntegerField(default = 0)
    online_time         = models.IntegerField(default = 0)
    invites             = models.IntegerField(default = 0)
    user_share          = models.IntegerField(default = 0)
    share_begin_time    = models.DateField(null = True, blank = True)
    active_time         = models.DateTimeField(u'激活时间',null = True, blank = True)
    last_lan_ip = models.CharField(max_length=50L, blank=True)
    is_active           = models.BooleanField(u'用户状态',default=True)
    is_staff            = models.BooleanField(u'后台登陆',default=False)

    class Meta:
        db_table = 'kx_user'
        verbose_name = (u'用户')
        verbose_name_plural = (u'用户')

    objects = KxUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nick']
 
    def get_full_name(self):
        return self.email
 
    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email
    #@property
    #def is_active(self):
    #    return self.status



class KxUserFriend(models.Model):
    user        = models.CharField(max_length = 50L, blank = True)
    friend      = models.CharField(max_length = 50L, blank = True)
    create_time = models.DateTimeField()
    id          = models.IntegerField(primary_key = True)
    class Meta:
        db_table = 'kx_user_friend'

class KxUserOrg(models.Model):
    id          = models.IntegerField(primary_key = True)
    user_id     = models.CharField(max_length=32L)
    org_id      = models.IntegerField()
    ent_id      = models.IntegerField()
    update_time = models.DateTimeField()
    updater_id  = models.CharField(max_length=32L)
    class Meta:
        db_table = 'kx_user_org'

class KxUserlogin(models.Model):
    id      = models.IntegerField(primary_key = True)
    email   = models.CharField(max_length = 50L)
    mac     = models.CharField(max_length = 100L)
    lan_ip  = models.CharField(max_length=50L, blank=True)
    wlan_ip = models.CharField(max_length=50L, blank=True)
    class Meta:
        unique_together = ("email", "mac")
        db_table = 'kx_userlogin'

class UserMsg(models.Model):
    user       = models.CharField(max_length = 50L, blank = True)
    title      = models.CharField(max_length = 50L, blank = True)
    content    = models.CharField(max_length = 2000L, blank = True)
    from_email = models.CharField(max_length = 50L)
    class Meta:
        db_table = 'user_msg'


