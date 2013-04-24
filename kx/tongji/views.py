#_*_coding:utf-8_*_
# Create your views here.

from django.http import Http404
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render_to_response,render
from django.http import HttpResponse, HttpResponseRedirect
from kx.models import (KxUser,KxMsgBoard,KxSoftRecord,KxTongjiRecord,KxLoginRecord)
from kx.models import (KxSoftBug,KxPub,KxPubTongji)
from django.contrib import auth,messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Max,Min
import datetime,logging
from dateutil.parser import parse
from utils import CustomSQL,bug_chart_sql

logger = logging.getLogger(__name__)

def tongji(request):
    try:
        if request.method == 'GET':
            today = datetime.date.today()
            tp = request.GET.get('type',1)
            day = request.GET.get('day',today)
            logger.info('type:%s day:%s',tp,day)
            if not request.user.is_superuser:
                return HttpResponseRedirect(reverse('index'))
            else:
                try:
                    login_num = KxUser.objects.extra(where=['DATE(last_login)=CURDATE()']).count()
                    logger.info('login_num:%d',login_num)
                except Exception as e:
                    login_num = 0
                    logger.debug(u'用户呢?%s',e)
                try:
                    all_user_num = KxSoftRecord.objects.filter(is_uninstall__exact=0).extra(select={'num':'count(DISTINCT client_identifie)'}).values('num')[0]['num']
                    #all_user_num = KxSoftRecord.objects.extra(select={'num':'count(distinct client_identifie)'}).filter(is_uninstall__exact=0)
                    logger.info('all_user_num:%s',all_user_num)
                except Exception as e:
                    all_user_num =0
                    logger.debug(u'有问题?%s',e)
                try:
                    max_login = KxTongjiRecord.objects.order_by('-all_num').values('tongji_day','all_num')[:1]
                    logger.info('max_login:%s',max_login)
                except Exception as e:
                    max_login =0
                    logger.debug(u'问题在那里?%s',e)
                if tp is not None and isinstance(tp,str):
                    try:
                        tp = int(tp.strip().strip('\t').strip('\n').strip('\r').strip('\0').strip('\x0B'))
                    except Exception as e:
                        logger.debug("%s",e)
                        tp =1
                if tp ==1:
                    if day is not None and isinstance(day,unicode):
                        try:
                            day =parse(day.strip().strip('\t').strip('\n').strip('\r').strip('\0').strip('\x0B'))
                        except Exception as e:
                            day = today
                            logger.debug("%s",e)
                try:
                    new_count = KxSoftRecord.objects.filter(is_new__exact=1,is_uninstall__exact=0).extra(where=['DATE(login_time)=%s'],params=[day]).extra(select={'num':'count(DISTINCT(client_identifie))'}).values('num')[0]['num']
                    logger.info("new_count:%s",new_count) 
                except Exception as e:
                    new_count =0
                    logger.debug("%s",e)

                try:
                    old_count = KxSoftRecord.objects.filter(is_new__exact=0,is_uninstall__exact=0).extra(where=['DATE(login_time)=%s'],params=[day]).extra(select={'num':'count(DISTINCT(client_identifie))'}).values('num')[0]['num']
                    logger.info("old_count:%s",old_count) 
                except Exception as e:
                    old_count =0
                    logger.deug("%s",e)

                try:
                    uninstall_num = KxSoftRecord.objects.filter(is_uninstall__exact=1).extra(where=['DATE(login_time)=%s'],params=[day]).extra(select={'num':'count(DISTINCT(client_identifie))'}).values('num')[0]['num']
                    logger.info("uninstall_num:%s",uninstall_num) 
                except Exception as e:
                    uninstall_num =0
                    logger.deug("%s",e)
                try:
                    new_user = KxUser.objects.extra(where=['DATE(last_login)=CURDATE()']).count()
                except Exception as e:
                    new_user = 0
                    logger.deug("%s",e)

                day_count = new_count + old_count
                temp_var={
                        'title':u'统计',
                        'domain':'simplenect.cn',
                        'login_num':login_num,
                        'all_user_num':all_user_num,
                        'type':tp,
                        'day':day,
                        'new_count':new_count,
                        'day_count':day_count,
                        'uninstall_num':uninstall_num,
                        'new_user':new_user,
                        'max_login_day':max_login[0]['tongji_day'],
                        'max_login_num':max_login[0]['all_num'],
                        }
        return render(request,"tongji.html",temp_var)
    except Exception as e:
        logger.debug("%s",e)
        raise Http404


def login_tongji(request):
    try:
        if request.method == 'GET':
            today = datetime.date.today()
            day = request.GET.get('day',today)
            if day is not None and isinstance(day,unicode):
                try:
                    day =parse(day.strip().strip('\t').strip('\n').strip('\r').strip('\0').strip('\x0B')).date()
                except Exception as e:
                    day = today
                    logger.debug("%s",e)
            if not request.user.is_superuser:
                return HttpResponseRedirect(reverse('index'))
            else:
                old_day = day-datetime.timedelta(days=29)
                day_list =[day-datetime.timedelta(days=d) for d in range(29,-1,-1)]
                #day_list = []
                #for d in range(29,-1,-1):
                #    day_list.append(day-datetime.timedelta(days=d))
                try:
                    login_dict = {}
                    login_list = KxLoginRecord.objects.filter(login_day__range=(old_day,day)).values('login_day','login_num')
                    for i in login_list:
                        login_dict[i['login_day']] = i['login_num']
                    for d in day_list:
                        if d not in login_dict.keys():
                            login_dict[d]=0
                    keys = login_dict.keys()
                    keys.sort()
                    login_l = [ login_dict[key] for key in keys]
                    logger.info("login_l:%s",login_l)
                except Exception as e:
                    logger.debug("%s",e)
                temp_var={
                        'title':u'统计',
                        'domain':'simplenect.cn',
                        'day':day,
                        'day_list':day_list,
                        'login_l':login_l,
                        }
                return render(request,"login_tongji.html",temp_var)
    except Exception as e:
        logger.debug("%s",e)
        raise Http404

def uninstall_chart(request):
    try:
        if request.method == 'GET':
            today = datetime.date.today()
            day = request.GET.get('day',today)
            if day is not None and isinstance(day,unicode):
                try:
                    day =parse(day.strip().strip('\t').strip('\n').strip('\r').strip('\0').strip('\x0B')).date()
                except Exception as e:
                    day = today
                    logger.debug("%s",e)
            if not request.user.is_superuser:
                return HttpResponseRedirect(reverse('index'))
            else:
                try:
                    sr_list = KxSoftRecord.objects.filter(is_uninstall__exact=1).extra(where=['DATE(login_time)=%s'],params=[day]).extra(select={'client_identifie':'client_identifie'}).values('client_identifie').annotate(login_time = Max('login_time')).order_by('-login_time')
                    logger.info("sr_list%s",sr_list)
                except Exception as e:
                    sr_list =0
                    logger.debug("sr_list:%s",e)
                sr_num = {}
                num_list = ["%02d" % i for i in range(23)]
                t_list = ["%02d" % i['login_time'].hour for i in sr_list ]
                client_list = [ i['client_identifie'] for i in sr_list ]
                #a = [ t_list.count(k) for k in num_list ]
                for k in num_list:
                    sr_num[k]=t_list.count(k)
                if len(client_list) > 0:
                    try:
                        f_list = KxSoftRecord.objects.filter(is_new__exact=1,client_identifie__in=client_list).extra(select={'client_identifie':'client_identifie'}).values('client_identifie').annotate(login_time = Min('login_time')).order_by()
                        logger.info("f_list%s",f_list)
                    except Exception as e:
                        logger.debug("%s",e)
                else:
                    f_list = 0
                temp_var={'title':u'统计',
                          'domain':'simplenect.cn',
                          'day':day,
                          'sr_list':sr_list,
                          'sr_num':sr_num,
                          'f_list':f_list, }
                return render(request,"uninstall_chart.html",temp_var)
    except Exception as e:
        logger.debug("%s",e)
        raise Http404



def bug_chart(request):
    try:
        if request.method == 'GET':
            today = datetime.date.today()
            day = request.GET.get('day',today)
            if day is not None and isinstance(day,unicode):
                try:
                    day =parse(day.strip().strip('\t').strip('\n').strip('\r').strip('\0').strip('\x0B')).date()
                except Exception as e:
                    day = today
                    logger.debug("%s",e)
            if not request.user.is_superuser:
                return HttpResponseRedirect(reverse('index'))
            else:
                #day = parse('2013-03-22').date()
                old_day = day-datetime.timedelta(days=29)
                day_list =[day-datetime.timedelta(days=d) for d in range(29,-1,-1)]
                #day_list = []
                #for d in range(29,-1,-1):
                #    day_list.append(day-datetime.timedelta(days=d))
                ######################################################
                try:
                    q ="""select count(*) as num,upload_date 
                          from (select client_identifie,date(upload_time) as upload_date 
                          from kx_soft_bug where date(upload_time) 
                          BETWEEN %s AND %s 
                          GROUP BY client_identifie,date(upload_time))t group by t.upload_date"""
                    p =[old_day,day]
                    bc_list = bug_chart_sql(q=q,p=p)
                except Exception as e:
                    logger.debug("%s",e)
                ######################################################
                try:
                    q ="""SELECT count(*) as num,login_date 
                          FROM (SELECT client_identifie,date(login_time) as login_date 
                          FROM  kx_soft_record where is_uninstall=0 and DATE(login_time)
                          BETWEEN %s AND %s 
                          GROUP BY client_identifie,date(login_time))t GROUP BY t.login_date"""
                    p =[old_day,day]
                    t_list = bug_chart_sql(q=q,p=p)
                except Exception as e:
                    logger.debug("%s",e)
                ######################################################
                '''客户端卸载'''
                try:
                    q ="""SELECT count(*) as num,login_date 
                          FROM (select client_identifie,date(login_time) as login_date 
                          FROM  kx_soft_record where is_uninstall=1 and date(login_time)  
                          BETWEEN %s and %s GROUP BY client_identifie,date(login_time))t group by t.login_date"""
                    unc_list = bug_chart_sql(q=q,p=p)
                except Exception as e:
                    logger.debug("%s",e)
                ######################################################
                try:
                    q ="""SELECT count(*) as num,login_date 
                          FROM (select client_identifie,DATE(login_time) as login_date 
                          FROM  kx_soft_record WHERE is_new=1 and DATE(login_time)  
                          BETWEEN %s AND %s 
                          GROUP BY client_identifie,DATE(login_time))t GROUP BY t.login_date"""
                    p =[old_day,day]
                    new_list = bug_chart_sql(q=q,p=p)
                except Exception as e:
                    logger.debug("%s",e)
                ######################################################
                try:
                    q = """select count(*) as num,date(create_time) as create_date 
                           from kx_user where date(create_time) 
                           between %s and %s group by date(create_time)"""
                    p =[old_day,day]
                    reg_list = bug_chart_sql(q=q,p=p)
                except Exception as e:
                    logger.debug("%s",e)

                temp_var={
                          'title':u'30天bug统计',
                          'domain':'simplenect.cn',
                          'day':day,
                          'day_list':day_list,
                          'bug_client':bc_list,
                          'bug_total':t_list,
                          'uninstall_client':unc_list,
                          'new_install':new_list,
                          'reg_list':reg_list,
                         }
                return render(request,"bug_chart.html",temp_var)
    except Exception as e:
        logger.debug("%s",e)
        raise Http404


def bug_msg(request):
    pass

def bug_log(request):
    pass


def reg_tongji(request):
    try:
        if request.method == 'GET':
            if not request.user.is_superuser:
                return HttpResponseRedirect(reverse('index'))
            else:
                temp_var = {}
                return render(request,"reg_tongji.html",temp_var)
    except Exception as e:
        logger.debug("%s",e)
        raise Http404

def reg_chart(request):
    try:
        if request.method == 'GET':
            if not request.user.is_superuser:
                return HttpResponseRedirect(reverse('index'))
            else:
                try:
                    pub_list = KxPub.objects.filter(is_tongji__exact=1).values('id','ver','pub_time')
                    logger.info("%s",pub_list)
                except Exception as e:
                    logger.debug("%s",e)
                try:
                    pt_list = KxPubTongji.objects.values('id','pub_id','reg_num','act_num','un_num')
                    logger.info("%s",pt_list)
                except Exception as e:
                    logger.debug("%s",e)
                reg_users = []
                inactive = []
                uninstall = []
                for i in pt_list:
                    reg_users.append(i['reg_num'])
                    inactive.append(i['reg_num']-i['act_num'])
                    uninstall.append(i['un_num'])
                temp_var = {
                            'title':u'24小时内新注册用户统计',
                            'domain':'simplenect.cn',
                            'pub_list':pub_list,
                            'reg_users':reg_users,
                            'inactive':inactive,
                            'uninstall':uninstall,
                        }
                return render(request,"reg_chart.html",temp_var)
    except Exception as e:
        logger.debug("%s",e)
        raise Http404

