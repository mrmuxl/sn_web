#_*_coding:utf-8_*_
# Create your views here.

from django.http import Http404
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render_to_response,render
from django.http import HttpResponse, HttpResponseRedirect
from apps.kx.models import (KxUser,KxMsgBoard,KxSoftRecord,KxTongjiRecord,KxLoginRecord)
from apps.kx.models import (KxPubTongji,KxLanDay,KxActTongji)
from apps.alipay.models import OrderInfo
from apps.publish.models import KxPub
from apps.bug_report.models import KxSoftBug
from django.contrib import auth,messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.db.models import Count,Max,Min
import datetime,logging,os
from dateutil.parser import parse
from utils import CustomSQL,bug_chart_sql
from django.conf import settings

logger = logging.getLogger(__name__)

@require_GET
def tongji(request):
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
            max_login = []
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
            new_user = KxUser.objects.extra(where=['DATE(create_time)=CURDATE()']).count()
        except Exception as e:
            new_user = 0
            logger.deug("%s",e)

        if max_login:
            max_login_day = max_login[0]['tongji_day']
            max_login_num = max_login[0]['all_num']
        else:
            max_login_day = 0
            max_login_num = 0
        day_count = new_count + old_count
        order_num = OrderInfo.objects.count()
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
                'max_login_day':max_login_day,
                'max_login_num':max_login_num,
                'order_num':order_num,
                }
        return render(request,"tongji.html",temp_var)


@require_GET
def login_tongji(request):
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
            login_list = KxLoginRecord.objects.filter(login_day__range=(old_day,day)).order_by('id').values('login_day','login_num')
            for i in login_list:
                login_dict[i['login_day']] = i['login_num']
            for d in day_list:
                if d not in login_dict.keys():
                    login_dict[d]=0
            #keys = login_dict.keys()
            #keys.sort()
            #login_l = [ login_dict[key] for key in keys]
            login_l = [ login_dict[key] for key in sorted(login_dict.keys())]
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

@require_GET
def uninstall_chart(request):
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
            sr_list = []
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
                f_list = []
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

@require_GET
def bug_chart(request):
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
            bc_list = []
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
            t_list = []
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
            unc_list = []
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
            new_list = []
            logger.debug("%s",e)
        ######################################################
        try:
            q = """select count(*) as num,date(create_time) as create_date 
                   from kx_user where date(create_time) 
                   between %s and %s group by date(create_time)"""
            p =[old_day,day]
            reg_list = bug_chart_sql(q=q,p=p)
        except Exception as e:
            reg_list = []
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

@require_GET
def bug_msg(request):
    today = datetime.date.today()
    day =str(request.GET.get('day',today))
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))
    else:
        try:
            bug_list = KxSoftBug.objects.extra(where=['DATE(upload_time)=%s'],params=[day]).values()
        except Exception as e:
            bug_list = []
            logger.debug("%s",e)
        path_root = settings.MEDIA_ROOT
        path_date = day.replace('-','/')
        folder ='BugReport/' + path_date
        if not os.path.exists(path_root + folder):
            message ="""目录不存在！<A HREF="javascript:history.back()">返 回</A>"""
            return HttpResponse(message)
        else:
            file_info = {}
            for file_name in os.listdir(path_root + folder):
                file_path = path_root + folder + "/" + file_name
                ctime = os.path.getctime(file_path)
                size = os.path.getsize(file_path)
                file_info[file_name]={'ctime':ctime,'size':size}
        temp_var = {
                    'domain':u'simplenect.cn',
                    'bug_list':bug_list,
                    'folder':folder,
                    'file_info':file_info,
                    'day':day,
                    }
        return render(request,"bug_msg.html",temp_var)


@require_GET
def bug_log(request):
    today = datetime.date.today()
    day =str(request.GET.get('day',today))
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))
    elif 'type' in request.GET:
        tp = request.GET['type']
        if tp == 'c':
            client_log = settings.MEDIA_ROOT + u"BugLog/" + u"soft_bug_" + day + u".log"
            if not os.path.exists(client_log):
                return HttpResponse("""日志文件不存在！<A HREF="javascript:history.back()">返 回</A>""")
            with open(client_log) as f:
                try:
                    log = f.read().decode('gbk').encode('utf8').replace('\n','<br/>')
                except Exception as e:
                    logger.debug("%s",e)
                    f.seek(0)
                    log = f.read().replace('\n','<br/>')
        elif tp == 's':
            if day == str(today):
                server_log = settings.SERVER_LOG + u"udt4/app/qm_error.log"
            else:
                server_log = settings.SERVER_LOG + u"qm_logs/days/qm_error.log-" + day
            if not os.path.exists(server_log):
                return HttpResponse("""日志文件不存在！<A HREF="javascript:history.back()">返 回</A>""")
            with open(server_log) as f:
                    log = f.read().replace('\n','<br/>')
        else:
            return HttpResponse("""日志类型不正确！<A HREF="javascript:history.back()">返 回</A>""")
        return HttpResponse(log)
    return HttpResponse("""没有日志类型！<A HREF="javascript:history.back()">返 回</A>""")

    

@require_GET
def reg_tongji(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))
    else:
        temp_var = {}
        return render(request,"reg_tongji.html",temp_var)

@require_GET
def reg_chart(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))
    else:
        pub_list = KxPub.objects.filter(is_tongji__exact=1).values('id','ver','pub_time')
        logger.info("%s",pub_list)
        pt_list = KxPubTongji.objects.values('id','pub_id','reg_num','act_num','un_num')
        logger.info("%s",pt_list)
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


@require_GET
def bug_ratio_chart(request):
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
        try:
            bug_list = KxTongjiRecord.objects.filter(tongji_day__range=(old_day,day)).order_by('id').values('id','seven_new_num','seven_un_num','tongji_day')
        except Exception as e:
            bug_list = []
            logger.debug("%s",e)
        bug_ratio = []
        if len(bug_list) < 30:
            for i in range(30):
                try:
                    bug_ratio.append(round(float(bug_list[i]['seven_un_num'])*100/float(bug_list[i]['seven_new_num']),2))
                except Exception as e:
                    bug_ratio.append(0)
                    pass
        else:
            bug_ratio = [round(float(i['seven_un_num'])*100/i['seven_new_num'],2) for i in bug_list]
        temp_var = {
                    'day':day,
                    'day_list':day_list,
                    'bug_ratio':bug_ratio,
                }
        return render(request,"bug_ratio_chart.html",temp_var)

@require_GET
def lan_stack_chart(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))
    else:
        today = datetime.date.today()
        day = request.GET.get('day',today)
        if day is not None and isinstance(day,unicode):
            try:
                day =parse(day.strip().strip('\t').strip('\n').strip('\r').strip('\0').strip('\x0B')).date()
            except Exception as e:
                day = today
                logger.debug("%s",e)
        old_day = day-datetime.timedelta(days=29)
        day_list =[day-datetime.timedelta(days=d) for d in range(29,-1,-1)]
        lan_list = KxLanDay.objects.filter(tongji_day__range=(old_day,day)).order_by('id').values()
        tp = request.GET.get('type',u'1')
        num1 = []
        num2 = []
        num3 = []
        num4 = []
        num5 = []
        num6 = []
        num7 = []
        lan_dict = {}
        if tp == '1':
            type_name =u"装机数"
            for i in range(30):
                try:
                    num1.append(lan_list[i]['qm1'])
                    num2.append(lan_list[i]['qm2'])
                    num3.append(lan_list[i]['qm3'])
                    num4.append(lan_list[i]['qm4'])
                    num5.append(lan_list[i]['qm5'])
                    num6.append(lan_list[i]['qm6'])
                    num7.append(lan_list[i]['qm7'])
                except Exception as e:
                    num1.append(0)
                    num2.append(0)
                    num3.append(0)
                    num4.append(0)
                    num5.append(0)
                    num6.append(0)
                    num7.append(0)
                    pass
        else:
            tp = '2'
            type_name =u"PC数"
            for i in range(30):
                try:
                    num1.append(lan_list[i]['pc1'])
                    num2.append(lan_list[i]['pc2'])
                    num3.append(lan_list[i]['pc3'])
                    num4.append(lan_list[i]['pc4'])
                    num5.append(lan_list[i]['pc5'])
                    num6.append(lan_list[i]['pc6'])
                    num7.append(lan_list[i]['pc7'])
                except Exception as e:
                    num1.append(0)
                    num2.append(0)
                    num3.append(0)
                    num4.append(0)
                    num5.append(0)
                    num6.append(0)
                    num7.append(0)
                    pass
        lan_dict['num1'] = num1
        lan_dict['num2'] = num2
        lan_dict['num3'] = num3
        lan_dict['num4'] = num4
        lan_dict['num5'] = num5
        lan_dict['num6'] = num6
        lan_dict['num7'] = num7
        t_var = {
                'domain':'simplenect.cn',
                'day':str(day),
                'type':tp,
                'type_name':type_name,
                'day_list':day_list,
                'lan_dict':lan_dict,
        }
        return render(request,"lan_stack_chart.html",t_var)

@require_GET
def lan_line_chart(request):
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
        try:
            lan_list = KxLanDay.objects.filter(tongji_day__range=(old_day,day)).order_by('id').values('id','lan_num','tongji_day')
        except Exception as e:
            lan_list = []
            logger.debug("%s",e)
        lan_line = []
        if len(lan_list) < 30:
            for i in range(30):
                try:
                    lan_line.append(lan_list[i]['lan_num'])
                except Exception as e:
                    lan_line.append(0)
                    pass
        else:
            lan_ratio = [i['lan_num'] for i in bug_list]
        t_var = {
                'domain':'simplenect.cn',
                'day':str(day),
                'day_list':day_list,
                'lan_list':lan_line,
        }
        return render(request,"lan_line_chart.html",t_var)

@require_GET
def silence_ratio_chart(request):
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
        users =KxUser.objects.all()
        active_users = users.filter(status__exact=1).count()
        no_active_users = users.filter(status__exact=0).count()
        bug_list = KxTongjiRecord.objects.filter(tongji_day__range=(old_day,day)).values('id','no_login_num','tongji_day')
        silence_ratio = []
        if len(bug_list) < 30:
            for i in range(30):
                try:
                    silence_ratio.append(round(float(bug_list[i]['no_login_num'])*100/acitve_users,2))
                except Exception as e:
                    silence_ratio.append(0)
                    pass
        else:
            silence_ratio = [round(float(i['no_login_num'])*100/active_users,2) for i in bug_list]
        t_var = {
                'domain':'simplenect.cn',
                'day':str(day),
                'day_list':day_list,
                'active_users':active_users,
                'no_active_users':no_active_users,
                'silence_ratio':silence_ratio,
        }
        return render(request,"silence_ratio_chart.html",t_var)

@require_GET
def remain_ratio_chart(request):
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
        bug_list = KxTongjiRecord.objects.filter(tongji_day__range=(old_day,day)).order_by('id').values('id','cur_mon_num','last_mon_num','tongji_day')
        remain_ratio = []
        if len(bug_list) < 30:
            for i in range(30):
                try:
                    remain_ratio.append(round(float(bug_list[i]['cur_mon_num'])*100/float(bug_list[i]['last_mon_num']),2))
                except Exception as e:
                    remain_ratio.append(0)
                    pass
        else:
            remain_ratio = [round(float(i['cur_mon_num'])*100/i['last_mon_num'],2) for i in bug_list]
        t_var = {
                'domain':'simplenect.cn',
                'day':str(day),
                'day_list':day_list,
                'remain_ratio':remain_ratio,
                }
        return render(request,"remain_ratio_chart.html",t_var)

@require_GET
def online_act_chart(request):
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
        online_list = KxActTongji.objects.filter(tongji_day__range=(old_day,day)).order_by('id').values('id','tongji_day','on_num','act_num','un_num')
        on_num = []
        act_num = []
        un_num = []
        if online_list:
            for i in range(30):
                try:
                    on_num.append(online_list[i]['on_num'])
                    act_num.append(online_list[i]['act_num'])
                    un_num.append(online_list[i]['un_num'])
                except Exception as e:
                    on_num.append(0)
                    act_num.append(0)
                    un_num.append(0)
                    pass
        else:
            on_num = act_num = un_num = [0 for i in range(30)] 
        t_var = {
                'domain':'simplenect.cn',
                'day':str(day),
                'day_list':day_list,
                'on_num':on_num,
                'act_num':act_num,
                'un_num':un_num,
                }
        return render(request,"online_act_chart.html",t_var)
        
