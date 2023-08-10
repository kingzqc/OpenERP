# Create your views here.
from __future__ import unicode_literals
import os
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
#
from django.shortcuts import render,redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from datetime import datetime,timedelta
#from django.utils import timezone as datetime
from base.models import *
from doc.models import *
from crm.models import *
from workflow.models import *
from base import forms
from django.contrib import messages
# user register start
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
UserProfile = get_user_model()
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from captcha.fields import CaptchaField # PSM add
# user register  end
from random import randint
import logging
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
#
def index(request):
    """Home page"""
    _form_data = {}  # 回传参数
    # 获取搜索框参数
    try:
        # 按钮条件筛选值
        typetop_list = []
        typedetail_list = []
        jobtype_list = []
        rm =''
        # ContentType_class='T' 代表获取 主题 类的信息
        for contenttype in ContentType.objects.filter(ContentType_class='TOPIC', Data_status='OK').order_by("Data_id"):
            if contenttype.is_pagetop == False:
                ct = {}
                ct['brief'] = contenttype.ContentType_brief
                ct['urlkey'] = contenttype.ContentType_urlkey
                ct['tag'] = contenttype.ContentType_tag
                ct['detail'] = contenttype.ContentType_detail
                ct['image'] = settings.MEDIA_URL + str(contenttype.ContentType_image)
                typedetail_list.append(ct)
            else:
                ct = {}
                ct['brief'] = contenttype.ContentType_brief
                ct['urlkey'] = contenttype.ContentType_urlkey
                ct['tag'] = contenttype.ContentType_tag
                ct['detail'] = contenttype.ContentType_detail
                ct['image'] = settings.MEDIA_URL + str(contenttype.ContentType_image)
                typetop_list.append(ct)
        for jobtype in JobType.objects.filter(Data_status='OK', is_pagetop=False).order_by("-Data_id"):
            jt ={}
            jt['code'] = jobtype.JobType_code
            jt['name'] = jobtype.JobType_content
            jobtype_list.append(jt)

        return render(request, "index.html", {
            'typetop_list': typetop_list,
            'typedetail_list': typedetail_list,
            'jobtype_list': jobtype_list,
            'response_message': rm,
        })
    except Exception as e:
        _form_data['exceptions'] = e
        _form_data['error_message'] = str(e)
        _form_data['request_feature'] = 'index'
        return render(request, "index.html", {
            'form_data': _form_data,
            'requestUrl': reverse('index'),
        })
#
def topicdetail(request):
    """Topic detail page"""
    topicurl = request.GET.get('topic', '')  # 资源 topic url
    _form_data = {}  # 回传参数
    try:
        # 按钮条件筛选值
        topictop = []
        topicdetail_list = []

        rm = ''
        flag = int(0) # 判断奇偶，HTML使用不同格式
        # TOPIC 页头图片及标签
        cc = ContentClass.objects.filter(ContentClass_brief="TOPIC", Data_status='OK')
        if cc:
            ct = {}
            ct['image'] = settings.MEDIA_URL + str(cc[0].ContentClass_image)
            ct['subject'] = cc[0].ContentClass_description
            topictop.append(ct)
        #
        rt = ContentType.objects.filter(ContentType_urlkey=topicurl, Data_status='OK')
        if rt:
            for resource in ResourceMaster.objects.filter(Resource_type=rt[0].Data_id, Data_status='OK', on_webpage=True).order_by("-Data_id"):
                ct = {}
                ct['topic'] = topicurl
                # 获取 关注和点赞 信息
                ui = UserInterest.objects.filter(User_interest=resource.Data_id, Data_status='OK').count()
                if ui:
                    ct['interest'] = ui
                else:
                    ct['interest'] = 0
                ut = UserThumbup.objects.filter(User_thumbup=resource.Data_id, Data_status='OK').count()
                if ut:
                    ct['thumbup'] = ut
                else:
                    ct['thumbup'] = 0
                #
                if resource.is_pagetop == False:
                    ct['dataid'] = resource.Data_id
                    ct['nickname'] = resource.Resource_nickname
                    ct['brief'] = resource.Resource_brief
                    ct['owner'] = resource.Data_owner
                    ct['docdate'] = resource.Data_datetime
                    ct['feature'] = resource.Resource_feature
                    ct['value'] = resource.Resource_value
                    ct['summary'] = resource.Resource_summary
                    ct['image'] = settings.MEDIA_URL + str(resource.Resource_image)
                    topicdetail_list.append(ct)

        return render(request, "topicdetail.html", {
            'topictop_list': topictop,
            'topicdetail_list': topicdetail_list,
            'response_message': rm,
        })
    except Exception as e:
        _form_data['exceptions'] = e
        _form_data['error_message'] = str(e)
        _form_data['request_feature'] = 'topicdetail'
        return render(request, "topicdetail.html", {
            'form_data': _form_data,
            'requestUrl': reverse('topicdetail'),
        })
#
def resource(request):
    """resources page"""
    _form_data = {}  # 回传参数
    rm = ''  # 响应
    # 获取GET参数
    page = request.GET.get('page', 1)
    data_id = request.GET.get('data_id', '')
    # 获取搜索框参数
    try:
        # 按钮条件筛选值
        resourcetop = []
        resourcedetail_list = []

        rm = ''
        # TOPIC 页头图片及标签
        cc = ContentClass.objects.filter(ContentClass_brief="RESOURCE", Data_status='OK')

        if cc:
            ct = {}
            ct['image'] = settings.MEDIA_URL + str(cc[0].ContentClass_image)
            ct['subject'] = cc[0].ContentClass_description
            resourcetop.append(ct)

        flag = int(0) # 判断奇偶，HTML使用不同格式
        if data_id:
            rm = ResourceMaster.objects.filter(Data_id=data_id, Data_status='OK', on_webpage=True).order_by( "-Data_id")
        else:
            rm = ResourceMaster.objects.filter(Resource_type__ContentType_class="RESOURCE", Data_status='OK', on_webpage=True).order_by(
                "-Data_id")
        for resource in rm:
            ct = {}
            # 获取 关注和点赞 信息
            #
            ui = UserInterest.objects.filter(User_myself=request.user.id,User_interest=resource.Data_id, Data_status='OK')
            if ui:
                ct['interest'] = 1
            else:
                ct['interest'] = 0
            ut = UserThumbup.objects.filter(User_myself=request.user.id, User_thumbup=resource.Data_id, Data_status='OK')
            if ut:
                ct['thumbup'] = 1
            else:
                ct['thumbup'] = 0
            #
            if resource.is_pagetop == False:
                if (flag % 2) == 0:
                    ct['flag'] = 0
                else:
                    ct['flag'] = 1
                flag +=1
                ct['dataid'] = resource.Data_id
                ct['nickname'] = resource.Resource_nickname
                ct['basecity'] = resource.Resource_basecity
                ct['contactinfo'] = resource.Resource_contactinfo
                ct['brief'] = resource.Resource_brief
                ct['feature'] = resource.Resource_feature
                ct['value'] = resource.Resource_value
                ct['dummyid'] = resource.Dummy_id
                ct['image'] = settings.MEDIA_URL + str(resource.Resource_image)
                resourcedetail_list.append(ct)

        return render(request, "resource.html", {
            'resourcetop_list': resourcetop,
            'resourcedetail_list': resourcedetail_list,
            'response_message': rm,
        })
    except Exception as e:
        _form_data['exceptions'] = e
        _form_data['error_message'] = str(e)
        _form_data['request_feature'] = 'resource'
        return render(request, "resource.html", {
            'form_data': _form_data,
            'requestUrl': reverse('resource'),
        })
#
def jobs(request):
    """services page"""
    _form_data = {}  # 回传参数
    rm = ''  # 响应
    # 获取GET参数
    resourcedummy = request.GET.get('resource_dummy', '') # resource id
    jobdummy = request.GET.get('service_dummy', '')  # job id
    # 获取搜索框参数
    try:
        # 按钮条件筛选值
        jobstop = []
        jobsdetail_list = []
        # jobtop
        cc = ContentClass.objects.filter(ContentClass_brief="SERVICE", Data_status='OK')
        if cc:
            ct = {}
            ct['image'] = settings.MEDIA_URL + str(cc[0].ContentClass_image)
            ct['subject'] = cc[0].ContentClass_description
            jobstop.append(ct)
        #
        if jobdummy:
            for job in JobMaster.objects.filter(Dummy_id=jobdummy, Data_status='OK', on_webpage=True).order_by("-Data_id"):
                if job.is_pagetop == False:
                    ct = {}
                    ct['jobid'] = job.Data_id
                    ct['jobname'] = job.Job_code
                    ct['jobowner'] = job.Data_owner
                    ct['jobtype'] = job.Job_type
                    ct['jobprice'] = job.Job_price
                    ct['jobbrief'] = job.Job_brief
                    ct['jobfeature'] = job.Job_feature
                    ct['jobtarget'] = job.Job_target
                    ct['dummyid'] = job.Dummy_id
                    ct['image'] = settings.MEDIA_URL + str(job.Job_image)
                    jobsdetail_list.append(ct)
        else:
            if resourcedummy:
                # get DataID
                dataid = ResourceMaster.objects.get(Dummy_id=resourcedummy).Data_id
                #
                for job in JobMaster.objects.filter(Job_resource=dataid, Data_status='OK', on_webpage=True).order_by("-Data_id"):
                    if job.is_pagetop == False:
                        ct = {}
                        ct['jobid'] = job.Data_id
                        ct['jobname'] = job.Job_code
                        ct['jobowner'] = job.Data_owner
                        ct['jobtype'] = job.Job_type
                        ct['jobprice'] = job.Job_price
                        ct['jobbrief'] = job.Job_brief
                        ct['jobfeature'] = job.Job_feature
                        ct['jobtarget'] = job.Job_target
                        ct['dummyid'] = job.Dummy_id
                        ct['image'] = settings.MEDIA_URL + str(job.Job_image)
                        jobsdetail_list.append(ct)
            else:
                for job in JobMaster.objects.filter(Data_status='OK', on_webpage=True).order_by("-Data_id"):
                    if job.is_pagetop == False:
                        ct = {}
                        ct['jobid'] = job.Data_id
                        ct['jobid'] = job.Data_id
                        ct['jobname'] = job.Job_code
                        ct['jobowner'] = job.Data_owner
                        ct['jobtype'] = job.Job_type
                        ct['jobprice'] = job.Job_price
                        ct['jobbrief'] = job.Job_brief
                        ct['jobfeature'] = job.Job_feature
                        ct['jobtarget'] = job.Job_target
                        ct['dummyid'] = job.Dummy_id
                        ct['image'] = settings.MEDIA_URL + str(job.Job_image)
                        jobsdetail_list.append(ct)

        return render(request, "jobs.html", {
            'jobstop_list': jobstop,
            'jobsdetail_list': jobsdetail_list,
            'response_message': rm,
        })
    except Exception as e:
        _form_data['exceptions'] = e
        _form_data['error_message'] = str(e)
        _form_data['request_feature'] = 'jobs'
        return render(request, "jobs.html", {
            'form_data': _form_data,
            'requestUrl': reverse('jobs'),
        })
#
def about(request):
    """About us page"""
    _form_data = {}  # 回传参数
    rm = ''  # 响应
    # 获取搜索框参数
    try:
        # 按钮条件筛选值
        abouttop = []
        aboutdetail_list = []

        rm = ''
        # TOPIC 页头图片及标签
        cc = ContentClass.objects.filter(ContentClass_brief="ABOUT", Data_status='OK')
        if cc:
            ct = {}
            ct['image'] = settings.MEDIA_URL + str(cc[0].ContentClass_image)
            ct['subject'] = cc[0].ContentClass_description
            abouttop.append(ct)

        flag = int(0)  # 判断奇偶，HTML使用不同格式
        for resource in ContentType.objects.filter(ContentType_class="ABOUT", Data_status='OK').order_by("-Data_id"):
            ct = {}
            #
            if resource.is_pagetop == False:
                if (flag % 2) == 0:
                    ct['flag'] = 0
                else:
                    ct['flag'] = 1
                flag += 1
                ct['dataid'] = resource.Data_id
                ct['brief'] = resource.ContentType_brief
                ct['detail'] = resource.ContentType_detail
                ct['image'] = settings.MEDIA_URL + str(resource.ContentType_image)
                aboutdetail_list.append(ct)

        return render(request, "about.html", {
            'abouttop_list': abouttop,
            'aboutdetail_list': aboutdetail_list,
            'response_message': rm,
        })
    except Exception as e:
        _form_data['exceptions'] = e
        _form_data['error_message'] = str(e)
        _form_data['request_feature'] = 'about'
        return render(request, "about.html", {
            'form_data': _form_data,
            'requestUrl': reverse('about'),
        })
#
def single(request):
    """Single page"""
    pass
    return render(request, 'single.html')
#
def agenda(request):
    """Agenda page"""
    resourcedummy = request.GET.get('resource_dummy', '') # 资源 data id
    if not resourcedummy:
        resource_id = request.user.id
    else:
        resource_id = ResourceMaster.objects.get(Dummy_id=resourcedummy).Data_id
    rm = ''
    agendatop = []
    # AGENDA 页头图片及标签
    cc = ContentClass.objects.filter(ContentClass_brief="WORKFLOW", Data_status='OK')
    if cc:
        ct = {}
        ct['image'] = settings.MEDIA_URL + str(cc[0].ContentClass_image)
        ct['subject'] = cc[0].ContentClass_description
        agendatop.append(ct)

    return render(request, 'agenda.html', {
            'resource_id': resource_id,
            'agendatop_list': agendatop,
            'response_message': rm,})
# 编辑 日程 可预约和取消
def editagenda(request):
    # 获取搜索框参数
    resource_id = int(request.GET.get('resource_id', '')) # 资源 ID
    month_firstday = request.GET.get('monthfirstday', '')
    month_lastday = request.GET.get('monthlastday', '')
    rm = ''
    try:
        data = {}
        linelist = []
        # 获取资源信息 by resource_id
        resource = ResourceMaster.objects.get(Data_id=resource_id, Data_status='OK')
        resourcename = resource.Resource_nickname
        #
        data['agendadate'] = month_lastday
        #获取当前日期
        currentdate = datetime.now().strftime('%Y-%m-%d')
        #
        resource_type = resource.Resource_type_id
        agendatype = ContentType.objects.filter(Data_id=resource_type, Content_shape__range=['HUMAN','SPACE'], Data_status='OK')
        if agendatype:
            # 获取能力/预约信息 存入 line_list 返回页面
            code = '0'
            bookedinittime = 0
            bookedendtime = 0
            agendalinelist = BaseCompetence.objects.filter(BaseCompetence_type=agendatype[0].Data_id, Data_status='OK').order_by("BaseCompetence_timestart","-BaseCompetence_timeend",)
            for agendaline in agendalinelist:
                line = {}
                line['dataid'] = agendaline.Data_id
                line['timestart'] = str(agendaline.BaseCompetence_timestart)
                line['timeend'] = str(agendaline.BaseCompetence_timeend)
                line['quantity'] = str(agendaline.BaseCompetence_quantity)
                fd = timezone.datetime.strptime(str(month_firstday),'%Y-%m-%d')
                ld = timezone.datetime.strptime(str(month_lastday), '%Y-%m-%d')
                daystart = fd.strftime('%Y-%m-%d')
                dayend = ld.strftime('%Y-%m-%d')
                datestart =timezone.datetime.strptime(daystart,'%Y-%m-%d')
                dateend = timezone.datetime.strptime(dayend,'%Y-%m-%d')
                #print(dayend,currentdate)
                bookinittime = agendaline.BaseCompetence_timestart
                bookendtime = agendaline.BaseCompetence_timeend
                rm = RequestMaster.objects.filter(Request_basecompetence_id=agendaline.Data_id, Request_mainresource_id__exact=resource_id,Request_initdate=datestart, Request_enddate=dateend, Request_cancel=0)
                if rm:
                    # 已经预定的开始结束时间
                    bookedinittime = rm[0].Request_inittime
                    bookedendtime = rm[0].Request_endtime
                    #
                    if dayend > currentdate:
                        if rm[0].Data_creator_id == request.user.id:
                            line['usage'] = '已约'  # 是否book的标识 Y/N
                            line['requestid'] = rm[0].Data_id  # 是否book的标识 Y/N
                            line['rcancel'] = 1 # 可以取消
                            line['rbook'] = 0  # 不可以预约
                        else:
                            line['usage'] = '已约'  # 是否book的标识 Y/N
                            line['requestid'] = rm[0].Data_id  # 是否book的标识 Y/N
                            line['rcancel'] = 0  # 不可以取消
                            line['rbook'] = 0  # 不可以预约
                            line['booker'] = rm[0].Data_creator_id  # 预约人
                    else:
                        line['usage'] = '已约'  # 是否book的标识 Y/N
                        line['requestid'] = rm[0].Data_id  # 是否book的标识 Y/N
                        line['rcancel'] = 0 # 不可以取消
                        line['rbook'] = 0  # 不可以预约
                        line['booker'] = rm[0].Data_creator_id  # 预约人
                    line['customerid'] = rm[0].Request_customer_id
                else:
                    if dayend > currentdate:
                        if bookedinittime==0 and bookedendtime==0:
                            line['usage'] = '可约'  # 是否book的标识 Y/N
                            line['requestid'] = 0
                            line['rbook'] = 1  # 可以预约
                            line['rcancel'] = 0  # 不可以取消
                        else:
                            if bookinittime >= bookedinittime and bookinittime <= bookedendtime and bookendtime >= bookedinittime and bookendtime <= bookedendtime:
                                line['usage'] = '停约'  # 是否book的标识 Y/N
                                line['requestid'] = 0
                                line['rbook'] = 0  # 不可以预约
                                line['rcancel'] = 0  # 不可以取消
                            else:
                                line['usage'] = '可约' # 是否book的标识 Y/N
                                line['requestid'] = 0
                                line['rbook'] = 1 # 可以预约
                                line['rcancel'] = 0  # 不可以取消
                    else:
                        line['usage'] = '停约'  # 是否book的标识 Y/N
                        line['requestid'] = 0
                        line['rbook'] = 0  # 不可以预约
                        line['rcancel'] = 0  # 不可以取消
                    line['customerid'] = 0
                linelist.append(line)
        else:
            code = '1'
        # 对于已经预约的时间段，包括该时间段的其它预约不能再被预约
        linelistbak = linelist
        for line in linelist:
            if line['rcancel']!=1:
                for linebak in linelistbak:
                    if linebak['timestart']>=line['timestart'] and linebak['timeend']<=line['timeend'] and linebak['rcancel']==1:
                        line['usage'] = '停约'  # 是否book的标识 Y/N
                        line['rbook'] = 0   # 不可以预约
        # 用户可选 客户 LIST
        customerlist = []
        cmlist = CustomerMaster.objects.filter(Data_bu=request.user.Data_bu)
        if cmlist:
            for customer1 in cmlist:
                customerline = {}
                customerline['customerid'] = str(customer1.Data_id)
                customerline['customername'] = customer1.Customer_name
                customerlist.append(customerline)
        #
        data = {
            "code": code,
            "linelist": linelist,
            "customerlist": customerlist,
            "agendadate": month_lastday,
            "resourcename": resourcename,
        }
        return JsonResponse(json.loads(json.dumps(data)))
    except Exception as e:
        return JsonResponse({'code': '1', 'msg': u'获取日程失败'})
#
def bookagenda(request):
    """ book Agenda """
    basecompetenceid = int(request.GET.get('basecompetence_id', '')) # base competence data id
    resourceid = int(request.GET.get('resource_id', ''))  # 资源 data id
    customerid = int(request.GET.get('customer_id', '0'))  # customer id
    clickdate = request.GET.get('click_date', '')  # 所选日期
    cd = timezone.datetime.strptime(str(clickdate), '%Y-%m-%d')
    rm = ''
    try:
        # 生成request流水号
        Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(100, 199))
        # 获取 基础能力的信息
        bc = BaseCompetence.objects.get(Data_id=basecompetenceid)
        if bc:
            timestart = bc.BaseCompetence_timestart
            timeend = bc.BaseCompetence_timeend
            duration = bc.BaseCompetence_quantity
        # 获取 资源的 owner 信息
        rm = ResourceMaster.objects.get(Data_id=resourceid)
        if rm:
            resourceowner = rm.Data_owner_id
        #  request 设置
        rmadd = RequestMaster.objects.filter(Dummy_id=Dummy_id)
        if rmadd:
            pass
        else:
            #
            up = UserProfile.objects.get(id=request.user.id)
            if resourceid == '':
                resourceid = up.defaultresource
            rt = RequestType.objects.filter(Data_bu_id=up.Data_bu_id, RequestType_code='APPOINTMENT').first()
            rmadd = RequestMaster()
            #
            rmadd.Dummy_id = Dummy_id
            rmadd.Request_usage = 'USR'
            rmadd.Request_type_id = rt.Data_id
            rmadd.Request_desc = 'WEB预订'
            rmadd.Request_account_id = request.user.id
            rmadd.Request_mainresource_id = resourceid
            rmadd.Request_initdate = cd
            rmadd.Request_enddate = cd
            rmadd.Request_inittime = str(timestart)
            rmadd.Request_endtime = str(timeend)
            rmadd.Request_duration = float(duration)
            rmadd.Request_basecompetence_id = basecompetenceid
            if customerid > 0:
                rmadd.Request_customer_id = customerid
            rmadd.Data_bu_id = up.Data_bu_id
            rmadd.Data_security = '10'
            rmadd.Data_owner_id = request.user.id
            rmadd.Data_creator_id = request.user.id
            rmadd.Data_approver_id = resourceowner
            rmadd.Data_processor_id = request.user.id
            rmadd.Data_realizer_id = request.user.id
            rmadd.Request_status = '00'
            rmadd.Request_comments = '请尽快确认'

            rmadd.save()
            code ='0'
        data = {
            "code": code,
            'msg': '预订 SUCESS!',
        }
        return JsonResponse(json.loads(json.dumps(data)))
    except Exception as e:
        return JsonResponse({'code': '1', 'msg': '预订 failed!'})
#
def cancelagenda(request):
    """Agenda page"""
    dataid = int(request.GET.get('data_id', '')) # 资源 data id
    rm = ''
    try:
        # 不希望相同的日程存在两个，get的结果只能有一个，否则报错
        request = RequestMaster.objects.get(Data_id=dataid, Data_creator=request.user.id, Request_status='00', Request_cancel=False)
        #print(request)
        if request:
            request.Request_status = ''
            request.Request_cancel = True
            request.save()
            code = '0'
        data = {
            "code": code,
            'msg': '取消 SUCESS!',
        }
        return JsonResponse(json.loads(json.dumps(data)))
    except Exception as e:
        return JsonResponse({'code': '1', 'msg': '取消 FAILED!'})
#
def load_agenda(request):
    # 获取搜索框参数
    resource_id = request.GET.get('data_id', '') # 资源 ID
    month_firstday = request.GET.get('monthfirstday', '')
    month_lastday = request.GET.get('monthlastday', '')
    #
    start_date = datetime.strptime(month_firstday, '%Y-%m-%d')
    end_date = datetime.strptime(month_lastday, '%Y-%m-%d')
    #print(start_date, end_date)
    try:
        data = {}
        idate = start_date
        request_date_list = []
        request_qty_list = []
        request_usage_list = []
        while idate <= end_date:
            request_date_list.append(datetime.strftime(idate,'%Y-%m-%d'))
            idate = idate + timedelta(days=1)
        #print(datelist)
        rmlist = RequestMaster.objects.filter((Q(Data_owner_id__exact=resource_id ) | Q(Data_approver_id__exact=resource_id ) |
                                               Q(Data_realizer_id__exact=resource_id ) | Q(Data_processor_id__exact=resource_id )),
                                              Request_initdate__gte=start_date, Request_initdate__lte=end_date,Request_status__gt ='')
        if rmlist:
            code = '0'
            for request_date in request_date_list:
                req_count = 0
                requestusage_by_date = []
                for rm in rmlist:
                    init_date = datetime.strftime(rm.Request_initdate,'%Y-%m-%d')
                    if init_date == request_date:
                        req_count += 1
                        requestusage_by_date.append(rm.Request_usage)
                #
                request_qty_list.append(req_count)
                request_usage_list.append(requestusage_by_date)
            #
        else:
            code = '1'
            idate = start_date
            while idate <= end_date:
                request_qty_list.append(0)
                request_usage_list.append(' ')
                idate = idate + timedelta(days=1)
            #print(request_usage_list)

        data = {
            "code": code,
            "datelist": request_date_list,
            "qtylist": request_qty_list,
            "usagelist": request_usage_list,
        }
        return JsonResponse(json.loads(json.dumps(data)))
    except Exception as e:
        return JsonResponse(code=-1, msg=u'获取日程失败', data=data)
#=========================================
class CustomBackend(ModelBackend):
    """
    用于base下的authenticate，
    setting中需配置全局路径AUTHENTICATION_BACKENDS，当用户登录验证时，用到base_login下的authenticate进行验证，会
    跳到此处进行验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):# 重写authenticate方法
        try:
            # 不希望用户存在两个，get的结果只能有一个，否则报错
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            # django的后台中密码是加密处理的，拿到客户登录的密码需要加密后才能对比判断，所以不能直接password==password
            # User继承的AbstractUser中有check_password（）方法，会直接将传入的密码加密后于后台的作比较:
            #print(user.check_password(password))
            if user:
                return user
        except Exception as e:
            return None
#
def base_login(request):
    """登录"""
    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        msg = "点击【登录】前，请检查填写的内容！"
        if login_form.is_valid():# form验证通过
            # 获取用户提交的用户名和密码
            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password', None)
            # 成功返回user对象,失败None
            user = authenticate(username=user_name, password=pass_word)
            # 如果不是null说明验证成功
            if user:
                if user.is_active:
                    # 只有注册激活才能登录
                    login(request, user)
                # request.session["is_login"] = True
                # request.session["username"] = user_name
                # request.session.set_expiry(5)
                    return redirect("/index/")
                else:
                    return render(request, 'login.html', {'msg': '用户未激活', 'login_form': login_form})
            # 账号或密码错误
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误','login_form': login_form})
        else:
            return render(request, 'login.html', {'msg': '请正确输入用户名及密码','login_form': login_form})
    else:
        login_form = forms.LoginForm() # 没有这句的情况下，前端页面没有初始内容
        return render(request, 'login.html', {'login_form': login_form})
    return render(request,'login.html')
#
def register(request):
    """用户注册"""
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            sur_name = request.POST.get('surname', None)
            name_name = request.POST.get('name', None)
            e_mail = request.POST.get('email', None)
            cell_phone = request.POST.get('cellphone', None)
            user_type = request.POST.get('usertype', None)
            resource_type = request.POST.get('resourcetype', None)
            data_bu = request.POST.get('databu', None)
            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password',None)
            pass_word = make_password(pass_word) # 密码加密后再保存
            # 生成 User流水号
            Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(900, 999))
            UserProfile.objects.create(
                first_name = name_name,
                last_name = sur_name,
                username=user_name,
                email=e_mail,
                mobile=cell_phone,
                usertype=user_type,
                Data_bu_id=data_bu,
                is_staff=True,
                is_active=True,
                password=pass_word,
                Dummy_id=Dummy_id,
            )
            # 获取新user的ID, 同时创建resource  DATE BY: 2023/05/24
            up = UserProfile.objects.filter(username=user_name).first()
            if up:
                userid = up.id
                # 生成 Resource 流水号
                Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(700, 799))
                #
                ResourceMaster.objects.create(Resource_code_id=userid,
                                              Resource_type_id=resource_type,
                                              Data_owner_id=userid,
                                              Data_coordinator_id=userid,
                                              Resource_nickname=user_name,
                                              Dummy_id=Dummy_id)
                # Resource创建后的DATA ID更新到User的默认资源中
                rm = ResourceMaster.objects.filter(Resource_code_id=userid, Data_owner_id=userid, Data_coordinator_id=userid, Resource_nickname=user_name).first()
                if rm:
                    UserProfile.objects.filter(username=user_name).update(defaultresource_id=rm.Data_id)
            #
            #send_mail.send_register_email(user_name,'register') # 发送邮件，用户激活账号
            messages.info(request, '登记 sucess!')
            return redirect('/login/')
        else:
            # register_form 已输入内容返回
            return render(request,'register.html',{'msg': register_form.errors,'register_form': register_form})
    else:
        register_form = forms.RegisterForm() # 没有这句的情况下，前端页面没有初始内容
        return render(request,'register.html',{'register_form':register_form})
    return render(request, 'register.html')
#
def base_logout(request):
    """退出登录"""
    logout(request)
    return render(request,'index.html')
#

def activeuser(request):
    """用户账号激活"""
    userid = request.GET.get('userid', '')  # 用户 userid
    if request.method == "GET":
        ac_record = UserProfile.objects.filter(id=userid,is_active=False)
        if ac_record:
            ac_email = ac_record[0].email
            ac_user = UserProfile.objects.get(email=ac_email)
            ac_user.is_active = True
            ac_user.save()
        else:
            return render(request,'activeresult.html',{'msg':'%s 用户不存在或者已经激活'% userid})
        email_count = ac_record[0].email
        return render(request,'activeresult.html',{'msg': '%s 用户激活成功'% userid})
#
def myprofile(request):
    """用户资料维护"""
    resourcedummy = request.GET.get('resource_dummy', '')  # 用户 data id
    userdummy = request.GET.get('user_dummy', '') # 用户 userid
    # 获取 user id
    userid = UserProfile.objects.get(Dummy_id=userdummy).id
    #
    if userid == request.user.id and request.user.is_authenticated:
        #
        if not resourcedummy:
            resource_id = UserProfile.objects.get(id=userid).defaultresource_id  # 如果为空，使用用户ID resource
        #
        if request.method == "GET":
            ac_record = UserProfile.objects.filter(id=userid)
            if ac_record:
                pass
            else:
                return render(request,'myself.html',{'msg':'%s 用户不存在或者已经激活'% userid})
            return render(request,'myself.html',{'resource_id': resource_id, 'user_dummy': userdummy,'msg': '%s 用户更新成功'% userid})
    else:
        return render(request, 'myself.html', {'msg': '%s 用户已经退出系统！' % userid})
#
@login_required()
def editprofile(request):
    """用户资料维护"""
    userdummy = request.GET.get('user_dummy', '') # 用户 userid
    if not userdummy:
        userdummy = request.POST.get('user_dummy', '')  # 用户 userid
    #
    if request.method == "GET":
        myprofile_form = {}
        user_profile = UserProfile.objects.filter(Dummy_id=userdummy)
        if user_profile:
            image = settings.MEDIA_URL + str(user_profile[0].image)
            username = user_profile[0].username
            userid = user_profile[0].id
            userdummy = user_profile[0].Dummy_id
            first_name = user_profile[0].first_name
            last_name = user_profile[0].last_name
            nick_name = user_profile[0].nick_name
            email = user_profile[0].email
            cellphone = user_profile[0].mobile
            birthday = user_profile[0].birthday
            #
            # 获取已有的数据，返回给前端页面
            myprofile_form ={
                'userdummy': userdummy,
                'image': image,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'nick_name': nick_name,
                'email': email,
                'cellphone': cellphone,
                'birthday': birthday,
            }
            #
            myprofile_form = forms.MyProfileForm(myprofile_form) # 没有这句话不体现form定义的格式
            return render(request, 'myprofile.html', {'msg': myprofile_form.errors, 'myprofile_form': myprofile_form, 'userdummy': userdummy, 'imageurl': image})
        else:
            myprofile_form = forms.MyProfileForm()
            return render(request,'myprofile.html',{'msg':'%s 用户还没有添加任何信息'% userdummy,'myprofile_form': myprofile_form, 'userdummy': userdummy})
    else:
        myprofile_form = forms.MyProfileForm(request.POST, request.FILES)
        if myprofile_form.is_valid():# form验证通过
            # 获取页面数据保存到数据库
            imageurl = ''
            image = request.FILES.get('image', None)
            if image:
                # image resize
                imageTemproary = Image.open(image)
                outputIoStream = BytesIO()
                imageTemproaryResized = imageTemproary.resize((400, 320))
                imageTemproaryResized.save(outputIoStream, format='JPEG', quality=85)
                outputIoStream.seek(0)
                image = InMemoryUploadedFile(outputIoStream, 'ImageField',
                                             "%s.jpg" % image.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(outputIoStream), None)
                # image upload path
                currentYM = str(datetime.now().strftime('%Y%m'))
                upload_to = 'static/base/static/website/image/' + currentYM
                media_root = settings.MEDIA_ROOT
                full_path = media_root + '/' + upload_to
                if not os.path.exists(full_path):  # 判断路径是否存在
                    os.makedirs(full_path)  # 创建此路径
                # 上传图片文件
                with open(full_path + '/' + image.name, 'wb') as f:
                    for c in image.chunks():  # 相当于切片
                        f.write(c)
                #
                imageurl = upload_to + '/' + image.name
            #
            username = request.POST.get('username', None)
            nickname = request.POST.get('nick_name', None)
            firstname = request.POST.get('first_name', None)
            lastname = request.POST.get('last_name', None)
            email = request.POST.get('email', None)
            cellphone = request.POST.get('cellphone', None)
            birthday = request.POST.get('birthday', None)
            #
            if UserProfile.objects.filter(username=username):
                if image:
                    UserProfile.objects.filter(username=username).update(image=imageurl, nick_name=nickname,
                                                                            first_name=firstname, last_name=lastname,
                                                                            email=email, mobile=cellphone, birthday=birthday)
                else:
                    UserProfile.objects.filter(username=username).update(nick_name=nickname,
                                                                            first_name=firstname, last_name=lastname,
                                                                            email=email, mobile=cellphone, birthday=birthday)
            else:
                up = UserProfile.objects.get(id=request.user.id)
                UserProfile.objects.create(image=imageurl,
                                           nick_name=nickname,
                                           first_name=firstname, last_name=lastname,
                                           email=email, mobile=cellphone, birthday=birthday, Data_bu_id=up.Data_bu_id)
            messages.info(request, '保存 sucess!')
            return redirect('/editprofile/?user_dummy=' + str(userdummy))
        else:
            #myprofile_form = forms.MyProfileForm()
            return render(request, 'myprofile.html', {'msg': myprofile_form.errors,'myprofile_form': myprofile_form, 'userdummy': userdummy,})
#
def forgotpassword(request):
    """忘记密码"""
    message ={}
    if request.method == "POST":
        forgot_form = forms.ForgotPasswordForm(request.POST)
        if forgot_form.is_valid():
            e_mail = request.POST.get('email', None)
            pass_word = request.POST.get('password', None)
            pass_word = make_password(pass_word)  # 密码加密后再保存
            user = UserProfile.objects.get(email=e_mail)
            user.password = pass_word
            user.save()
            return redirect('/login/')
        else:  # form表单验证不通过
            message['msg'] = '邮箱,手机或验证码错误'
            message['status'] = True
            return render(request,'forgotpassword.html',{'msg':forgot_form.errors,'forgot_form':forgot_form})

    else:
        forgot_form = forms.ForgotPasswordForm()
    return render(request,'forgotpassword.html',{'forgot_form':forgot_form})
#
def resetpassword(request,email):
    """用户重置密码链接"""

    if request.method =="GET":
        e_mail = email
        if e_mail:
            return render(request, "resetpassword.html", {"email": e_mail})
        else:# 链接不对
            return render(request, "forgotpassword.html")
    if request.method == "POST":
        reset_form = forms.ResetPasswordForm(request.POST)
        if reset_form.is_valid():
            pass_word = request.POST.get('password', None)
            pass_word = make_password(pass_word)  # 密码加密后再保存
            user = UserProfile.objects.get(email=email)
            user.password = pass_word
            user.save()
            return render(request, "login.html")
        else:  # form表单验证不通过
            return render(request,'resetpassword.html',{'msg':reset_form.errors,'reset_form':reset_form})
#
def modify_pwd(request):
    """重置密码"""
    if request.method == "POST":
        modify_form = forms.ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", None)
            pwd2 = request.POST.get("password2", None)
            email = request.POST.get("email", None)
            if pwd1 != pwd2:
                return render(request, "resetpassword.html", {"email": email, "msg": "密码不一致！"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", None)
            return render(request, "resetpassword.html", {"email": email, "modify_form": modify_form})
#
@login_required
#@permission_required('base.BU_ENABLE', login_url='/base/forbid/')
@csrf_exempt
def make_bu_enable(request):
    # 获取搜索框参数
    data = {}
    bucode = request.GET.get('BU_code', '')
    try:
        bum= BUMaster.objects.get(BU_code=bucode)
        if bum.BU_status != '00':
            messages.success(request, '%s 已经进行了初始化。' % bucode)
            return redirect('/psm/base/bumaster/')
        else:
            # 创建BU参数
            bp = BuParameter.objects.filter(Bu_code_id=bucode)
            if not bp:
                BuParameter.objects.create(Bu_paratype='industry', Bu_parakey='DFT',
                                           Bu_paravalue='默认', Data_security='10', Bu_code_id=bucode)
                BuParameter.objects.create(Bu_paratype='scale', Bu_parakey='DFT',
                                           Bu_paravalue='默认', Data_security='10', Bu_code_id=bucode)
                BuParameter.objects.create(Bu_paratype='service', Bu_parakey='DFT',
                                           Bu_paravalue='默认', Data_security='10', Bu_code_id=bucode)
            # 创建服务Item
            im = ItemMaster.objects.filter(Data_bu_id=bucode)
            if not im:
                ItemMaster.objects.create(Item_code='DFT', Item_desc='默认', Item_unit='EA',
                                          Item_baseprice=1.00, Data_security='10', Data_bu_id=bucode, Data_creator_id=request.user.id)
            # 创建流程目录
            rc = RequestCatalogue.objects.filter(Data_bu_id=bucode)
            if not rc:
                RequestCatalogue.objects.create(Catalogue_code='CAL', Catalogue_desc='日程', Catalogue_type='CAL',
                                                Catalogue_active=1, Catalogue_comments='系统必备', Data_security='10',
                                                Data_bu_id=bucode, Data_creator_id=request.user.id, Data_owner_id=request.user.id)
                RequestCatalogue.objects.create(Catalogue_code='CRM', Catalogue_desc='CRM', Catalogue_type='OPD',
                                                Catalogue_active=1, Catalogue_comments='系统必备', Data_security='10',
                                                Data_bu_id=bucode, Data_creator_id=request.user.id,
                                                Data_owner_id=request.user.id)
                RequestCatalogue.objects.create(Catalogue_code='PRJ', Catalogue_desc='交付', Catalogue_type='PRD',
                                                Catalogue_active=1, Catalogue_comments='系统必备', Data_security='10',
                                                Data_bu_id=bucode, Data_creator_id=request.user.id,
                                                Data_owner_id=request.user.id)
            # 创建日程/商机流程
            rt = RequestType.objects.filter(Data_bu_id=bucode)
            if not rt:
                rc = RequestCatalogue.objects.filter(Data_bu_id=bucode, Catalogue_type='CAL').first()
                RequestType.objects.create(RequestType_code='APPOINTMENT', RequestType_desc='日程预约',
                                           Request_mustcont=1, Request_mustcust=1, Request_mustoppo=1,
                                           Request_mustproj=1, Request_mustdocu=1, Request_mustitem=1,
                                           Request_creatorrole='self', Request_approverrole='self',
                                           Request_realizerrole='self', Request_processorrole='self',
                                           Request_reopenerrole='self', Request_backerrole='self',
                                           Request_deleterrole='self', Request_openoverdue=8,
                                           Request_approveoverdue=8, Request_realizeoverdue=8,
                                           Request_totaloverdue=24, RequestType_active=1,
                                           RequestType_comments='系统必备', Data_security='10', Data_bu_id=bucode,
                                           Data_creator_id=request.user.id, Data_owner_id=request.user.id,
                                           RequestType_catalogue_id=rc.Data_id
                                           )
                rc = RequestCatalogue.objects.filter(Data_bu_id=bucode, Catalogue_type='OPD').first()
                RequestType.objects.create(RequestType_code='PROSPECT', RequestType_desc='潜在客户',
                                           Request_mustcont=1, Request_mustcust=1, Request_mustoppo=1,
                                           Request_mustproj=1, Request_mustdocu=1, Request_mustitem=1,
                                           Request_creatorrole='self', Request_approverrole='self',
                                           Request_realizerrole='self', Request_processorrole='self',
                                           Request_reopenerrole='self', Request_backerrole='self',
                                           Request_deleterrole='self', Request_openoverdue=8,
                                           Request_approveoverdue=8, Request_realizeoverdue=8,
                                           Request_totaloverdue=24, RequestType_active=1,
                                           RequestType_comments='系统必备', Data_security='10', Data_bu_id=bucode,
                                           Data_creator_id=request.user.id, Data_owner_id=request.user.id,
                                           RequestType_catalogue_id=rc.Data_id
                                           )
                RequestType.objects.create(RequestType_code='QUALIFY', RequestType_desc='甄别线索',
                                           Request_mustcont=1, Request_mustcust=1, Request_mustoppo=1,
                                           Request_mustproj=1, Request_mustdocu=1, Request_mustitem=1,
                                           Request_creatorrole='self', Request_approverrole='self',
                                           Request_realizerrole='self', Request_processorrole='self',
                                           Request_reopenerrole='self', Request_backerrole='self',
                                           Request_deleterrole='self', Request_openoverdue=8,
                                           Request_approveoverdue=8, Request_realizeoverdue=8,
                                           Request_totaloverdue=24, RequestType_active=1,
                                           RequestType_comments='系统必备', Data_security='10', Data_bu_id=bucode,
                                           Data_creator_id=request.user.id, Data_owner_id=request.user.id,
                                           RequestType_catalogue_id=rc.Data_id
                                           )
                RequestType.objects.create(RequestType_code='QUOTATION', RequestType_desc='方案报价',
                                           Request_mustcont=1, Request_mustcust=1, Request_mustoppo=1,
                                           Request_mustproj=1, Request_mustdocu=1, Request_mustitem=1,
                                           Request_creatorrole='self', Request_approverrole='self',
                                           Request_realizerrole='self', Request_processorrole='self',
                                           Request_reopenerrole='self', Request_backerrole='self',
                                           Request_deleterrole='self', Request_openoverdue=8,
                                           Request_approveoverdue=8, Request_realizeoverdue=8,
                                           Request_totaloverdue=24, RequestType_active=1,
                                           RequestType_comments='系统必备', Data_security='10', Data_bu_id=bucode,
                                           Data_creator_id=request.user.id, Data_owner_id=request.user.id,
                                           RequestType_catalogue_id=rc.Data_id
                                           )
                RequestType.objects.create(RequestType_code='NEGOTIATE', RequestType_desc='商务协商',
                                           Request_mustcont=1, Request_mustcust=1, Request_mustoppo=1,
                                           Request_mustproj=1, Request_mustdocu=1, Request_mustitem=1,
                                           Request_creatorrole='self', Request_approverrole='self',
                                           Request_realizerrole='self', Request_processorrole='self',
                                           Request_reopenerrole='self', Request_backerrole='self',
                                           Request_deleterrole='self', Request_openoverdue=8,
                                           Request_approveoverdue=8, Request_realizeoverdue=8,
                                           Request_totaloverdue=24, RequestType_active=1,
                                           RequestType_comments='系统必备', Data_security='10', Data_bu_id=bucode,
                                           Data_creator_id=request.user.id, Data_owner_id=request.user.id,
                                           RequestType_catalogue_id=rc.Data_id
                                           )
                RequestType.objects.create(RequestType_code='CLOSING', RequestType_desc='签约',
                                           Request_mustcont=1, Request_mustcust=1, Request_mustoppo=1,
                                           Request_mustproj=1, Request_mustdocu=1, Request_mustitem=1,
                                           Request_creatorrole='self', Request_approverrole='self',
                                           Request_realizerrole='self', Request_processorrole='self',
                                           Request_reopenerrole='self', Request_backerrole='self',
                                           Request_deleterrole='self', Request_openoverdue=8,
                                           Request_approveoverdue=8, Request_realizeoverdue=8,
                                           Request_totaloverdue=24, RequestType_active=1,
                                           RequestType_comments='系统必备', Data_security='10', Data_bu_id=bucode,
                                           Data_creator_id=request.user.id, Data_owner_id=request.user.id,
                                           RequestType_catalogue_id=rc.Data_id
                                           )
            # 创建流程类型
            ft = FlowType.objects.filter(Data_bu_id=bucode)
            if not ft:
                FlowType.objects.create(Flowtype_code='STD', Flowtype_desc='标准商务流程', Flowtype_usage='CRM',
                                        Flowtype_active=1, Data_security='10', Data_bu_id=bucode,
                                        Data_creator_id=request.user.id,
                                        Data_owner_id=request.user.id)
                std = FlowType.objects.filter(Data_bu_id=bucode, Flowtype_code='STD')
                FlowType.objects.create(Flowtype_code='SHORT', Flowtype_desc='简短商务流程', Flowtype_usage='CRM',
                                        Flowtype_active=1, Data_security='10', Data_bu_id=bucode,
                                        Data_creator_id=request.user.id,
                                        Data_owner_id=request.user.id)
            #
            std = FlowType.objects.filter(Data_bu_id=bucode, Flowtype_code='STD').first()
            fcm = FlowCycleMaster.objects.filter(Data_bu_id=bucode, Flowcycle_type__Flowtype_code__exact='STD').first()
            if not fcm:
                rt1 = RequestType.objects.filter(Data_bu_id=bucode,RequestType_code='PROSPECT').first()
                FlowCycleMaster.objects.create(Flowcycle_stagedesc='客户挖掘', Data_security='10',
                                               Data_bu_id=bucode, Data_creator_id=request.user.id,
                                                Data_owner_id=request.user.id, Flowcycle_stage_id=rt1.Data_id, Flowcycle_type_id=std.Data_id)
                #
                rt2 = RequestType.objects.filter(Data_bu_id=bucode, RequestType_code='QUALIFY').first()
                FlowCycleMaster.objects.create(Flowcycle_stagedesc='甄别线索', Data_security='10',
                                               Data_bu_id=bucode, Data_creator_id=request.user.id,
                                               Data_owner_id=request.user.id, Flowcycle_stage_id=rt2.Data_id,
                                               Flowcycle_type_id=std.Data_id)
                #
                rt3 = RequestType.objects.filter(Data_bu_id=bucode, RequestType_code='QUOTATION').first()
                FlowCycleMaster.objects.create(Flowcycle_stagedesc='方案报价', Data_security='10',
                                               Data_bu_id=bucode, Data_creator_id=request.user.id,
                                               Data_owner_id=request.user.id, Flowcycle_stage_id=rt3.Data_id,
                                               Flowcycle_type_id=std.Data_id)
                #
                rt4 = RequestType.objects.filter(Data_bu_id=bucode, RequestType_code='NEGOTIATE').first()
                FlowCycleMaster.objects.create(Flowcycle_stagedesc='商务谈判', Data_security='10',
                                               Data_bu_id=bucode, Data_creator_id=request.user.id,
                                               Data_owner_id=request.user.id, Flowcycle_stage_id=rt4.Data_id,
                                               Flowcycle_type_id=std.Data_id)
                #
                rt5 = RequestType.objects.filter(Data_bu_id=bucode, RequestType_code='CLOSING').first()
                FlowCycleMaster.objects.create(Flowcycle_stagedesc='达成交易', Data_security='10',
                                               Data_bu_id=bucode, Data_creator_id=request.user.id,
                                               Data_owner_id=request.user.id, Flowcycle_stage_id=rt5.Data_id,
                                               Flowcycle_type_id=std.Data_id)
            #
            short = FlowType.objects.filter(Data_bu_id=bucode, Flowtype_code='SHORT').first()
            fcm = FlowCycleMaster.objects.filter(Data_bu_id=bucode, Flowcycle_type__Flowtype_code__exact='SHORT').first()
            if not fcm:
                rt3 = RequestType.objects.filter(Data_bu_id=bucode, RequestType_code='QUALIFY').first()
                FlowCycleMaster.objects.create(Flowcycle_stagedesc='了解需求', Data_security='10',
                                               Data_bu_id=bucode, Data_creator_id=request.user.id,
                                               Data_owner_id=request.user.id, Flowcycle_stage_id=rt3.Data_id,
                                               Flowcycle_type_id=short.Data_id)
                #
                rt4 = RequestType.objects.filter(Data_bu_id=bucode, RequestType_code='QUOTATION').first()
                FlowCycleMaster.objects.create(Flowcycle_stagedesc='报价', Data_security='10',
                                               Data_bu_id=bucode, Data_creator_id=request.user.id,
                                               Data_owner_id=request.user.id, Flowcycle_stage_id=rt4.Data_id,
                                               Flowcycle_type_id=short.Data_id)
                #
                rt5 = RequestType.objects.filter(Data_bu_id=bucode, RequestType_code='CLOSING').first()
                FlowCycleMaster.objects.create(Flowcycle_stagedesc='签约', Data_security='10',
                                               Data_bu_id=bucode, Data_creator_id=request.user.id,
                                               Data_owner_id=request.user.id, Flowcycle_stage_id=rt5.Data_id,
                                               Flowcycle_type_id=short.Data_id)
            messages.info(request, '亲，已经初始化的BU不能使用该功能。')
            return redirect('/psm/base/bumaster/')
    except Exception as e:
        return HttpResponse('程序出错了！')
#--------------------------------------------------------------
import json
from django.http import HttpResponse

# Create your views here.
def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
    json_str,
    content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
    "code": code,
    "msg": "success",
    "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
    "code": code,
    "msg": error_string,
    "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error

# ============================================================
import random
from base.models import EmailVerifyRecord
from django.core.mail import send_mail
from PSMProject import settings

def random_str(random_length=16):
    """默认生成16位随机字符串"""
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    ran_dom = random.Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str

# 发送邮件
def send_register_email(email, send_type="register"):
    """
    发送邮件
    发送前需要先保存到数据库，到时候查询链接是否存在
    """
    if send_type == 'update_email': # 修改密码操作
        code = random_str(4)

    else:
        code = random_str(16)

    # 保存到数据库
    EmailVerifyRecord.objects.create(
        code=code,
        email=email,
        send_type=send_type
    )

    # 定义邮箱内容：
    if send_type == "register":
        subject = "PSM注册激活链接"  # 标题
        email_body = "请复制打开下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)  # 文本邮件体
        sender = settings.DEFAULT_FROM_EMAIL  # 发件人
        receiver = [email]  # 接收人
        email_send_status = send_mail(subject, email_body, sender, receiver)
        return email_send_status
        # if email_send_status:
        #     pass
    elif send_type == 'forget':
        subject = "PSM重置密码链接"  # 标题
        email_body = "请复制打开下面的链接重置密码：http://127.0.0.1:8000/reset/{0}".format(code)  # 文本邮件体
        sender = settings.DEFAULT_FROM_EMAIL  # 发件人
        receiver = [email]  # 接收人
        email_send_status = send_mail(subject, email_body, sender, receiver)
        return email_send_status
#资源列表
@login_required()
def resource_list(request):
    _form_data = {}  # 回传参数
    _humanitems = []  # 回传列表
    _spaceitems = []  # 回传列表
    humanlovescount = []
    spacelovescount = []
    # 获取GET参数
    page = request.GET.get('page', 1)
    resourceowner = request.GET.get('data_id', '')
    userdummy = request.GET.get('user_dummy', '')
    # 获取 userid
    userid = UserProfile.objects.get(Dummy_id=userdummy).id
    # 获取搜索框参数
    try:
        _filter = {}
        # 按钮条件筛选值
        if userid !='' and userid != 'all':
            _filter['Data_owner'] = int(userid)
        #
        if resourceowner !='' and resourceowner != 'all':
            _filter['Data_owner'] = int(resourceowner)
        # 人力资源
        humanlist = ResourceMaster.objects.filter(**_filter, Resource_type__Content_shape__in=["HUMAN"]).order_by("Data_id")
        #
        _humanitems = humanlist
        # 空间资源
        spacelist = ResourceMaster.objects.filter(**_filter, Resource_type__Content_shape__in=["SPACE"]).order_by("Data_id")
        #
        _spaceitems = spacelist
        # 关注资源
        interest = UserInterest.objects.filter(User_myself=userid, Data_status='OK').values('User_interest')
        #
        interestlist = ResourceMaster.objects.filter(Data_id__in=interest).order_by("Data_id")
        _interestitems = interestlist
        # --页码-- 获取URL中除page外的其它参数
        query_string = re.sub(r'page=[0-9]+[&]?', '', request.META.get('QUERY_STRING', None))
        if query_string:
            query_string = '&' + query_string

        _form_data['total'] = _humanitems.count()

        for item in _humanitems:
            lc={}
            lc['key'] = item.Data_id
            if UserInterest.objects.filter(User_interest=item.Data_id, Data_status='00').count():
                lc['value'] = UserInterest.objects.filter(User_interest=item.Data_id, Data_status='00').count()
                humanlovescount.append(lc)
        #
        for item in _spaceitems:
            lc = {}
            lc['key'] = item.Data_id
            if UserInterest.objects.filter(User_interest_id=item.Data_id,
                                           Data_status='00').count():
                lc['value'] = UserInterest.objects.filter(User_interest_id=item.Data_id,
                                                          Data_status='00').count()
                spacelovescount.append(lc)
        #
        paginator = Paginator(_humanitems, 10)  # Show 20 contacts per page

        try:
            _items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            _items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            _items = paginator.page(paginator.num_pages)

        return render(request, "resourcelist.html", {
            'form_data': _form_data,
            'humanresourcelist': _humanitems,
            'spaceresourcelist': _spaceitems,
            'interestresourcelist': _interestitems,
            'humanloveslist': humanlovescount,
            'spaceloveslist': spacelovescount,
            'requestUrl': reverse('resourcelist'),
            'query_string': query_string,
            'paginator': paginator,
        })
    except Exception as e:
        return HttpResponse('程序出错了！')
#资源详情
@login_required()
def resource_detail_edit(request):
    """用户资料维护"""
    resourcedummy = request.GET.get('resource_dummy', '')  # 用户 data id
    #
    if request.method == "GET":
        resource_profile = ResourceMaster.objects.filter(Dummy_id=resourcedummy)
        if resource_profile:
            image = settings.MEDIA_URL + str(resource_profile[0].Resource_image)
            onwebpage = resource_profile[0].on_webpage
            nickname = resource_profile[0].Resource_nickname
            contactinfo = resource_profile[0].Resource_contactinfo
            resourcetype = resource_profile[0].Resource_type_id
            basecity = resource_profile[0].Resource_basecity
            #
            brief = resource_profile[0].Resource_brief
            feature = resource_profile[0].Resource_feature
            value = resource_profile[0].Resource_value
            summary = resource_profile[0].Resource_summary
            owner = resource_profile[0].Data_owner_id
            resourcecode = resource_profile[0].Resource_code_id
            # 获取已有的数据，返回给前端页面
            resourcedetail_form ={
                'mode': 'view',
                'nowuser': request.user.id,
                'resource_dummy': resourcedummy,
                'imageurl': image,
                'onwebpage': onwebpage,
                'nickname': nickname,
                'contactinfo': contactinfo,
                'resourcetype': resourcetype,
                'basecity': basecity,
                'brief': brief,
                'feature': feature,
                'value': value,
                'summary': summary,
                'owner': owner,
                'resourcecode': resourcecode,
            }
            #
            resourcedetail_form = forms.ResourceForm(resourcedetail_form) # 没有这句话不体现form定义的格式
            return render(request, 'resourcedetail.html', {'msg': resourcedetail_form.errors, 'resourcedetail_form': resourcedetail_form, 'resource_dummy': resourcedummy, 'imageurl': image})
        else:
            resourcedetail_form = {
                'mode': 'edit',
                'nowuser': request.user.id,
                'resource_dummy': '',
                'imageurl': '',
                'nickname': '',
                'contactinfo': '',
                'resourcetype': '',
                'basecity': '',
                'brief': '',
                'feature': '',
                'value': '',
                'summary': '',
                'owner': request.user.id,
                'resourcecode': '',
            }
            resourcedetail_form = forms.ResourceForm(resourcedetail_form)
            return render(request,'resourcedetail.html',{'msg':'请输入新增资源的内容','resourcedetail_form': resourcedetail_form, 'resource_dummy': resourcedummy})
    else:
        resourcedetail_form = forms.ResourceForm(request.POST, request.FILES)
        if resourcedetail_form.is_valid():# form验证通过
            # 获取页面数据保存到数据库
            imageurl = ''
            image = request.FILES.get('image', None)
            if image:
                # image resize
                imageTemproary = Image.open(image)
                outputIoStream = BytesIO()
                imageTemproaryResized = imageTemproary.resize((400, 320))
                imageTemproaryResized.save(outputIoStream, format='JPEG', quality=85)
                outputIoStream.seek(0)
                image = InMemoryUploadedFile(outputIoStream, 'ImageField',
                                             "%s.jpg" % image.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(outputIoStream), None)
                # image upload path
                currentYM = str(datetime.now().strftime('%Y%m'))
                upload_to = 'static/base/static/website/image/' + currentYM
                media_root = settings.MEDIA_ROOT
                full_path = media_root + '/' + upload_to
                if not os.path.exists(full_path):  # 判断路径是否存在
                    os.makedirs(full_path)  # 创建此路径
                # 上传图片文件
                with open(full_path + '/' + image.name, 'wb') as f:
                    for c in image.chunks():  # 相当于切片
                        f.write(c)
                #
                imageurl = upload_to + '/' + image.name
            #
            onwebpage = request.POST.get('onwebpage', None)
            nickname = request.POST.get('nickname', None)
            contactinfo = request.POST.get('contactinfo', None)
            resourcetype = int(request.POST.get('resourcetype', None))
            basecity = request.POST.get('basecity', None)
            brief = request.POST.get('brief', None)
            feature = request.POST.get('feature', None)
            value = request.POST.get('value', None)
            summary = request.POST.get('summary', None)
            owner = int(request.POST.get('owner', None))
            resourcecode = int(request.POST.get('resourcecode', None))
            #
            if onwebpage == 'on':
                onwebpage = True
            else:
                onwebpage = False
            #
            #
            if ResourceMaster.objects.filter(Dummy_id=resourcedummy):
                if image:
                    ResourceMaster.objects.filter(Dummy_id=resourcedummy).update(Resource_image=imageurl, Resource_nickname=nickname,
                                                                            Resource_contactinfo=contactinfo, Resource_type_id=resourcetype,
                                                                              Resource_basecity=basecity, on_webpage=onwebpage,
                                                                            Resource_brief=brief, Resource_feature=feature, Resource_value=value,
                                                                              Resource_summary=summary, Data_owner_id=owner, Resource_code_id=resourcecode)
                else:
                    ResourceMaster.objects.filter(Dummy_id=resourcedummy).update(Resource_nickname=nickname, on_webpage=onwebpage,
                                                                                    Resource_contactinfo=contactinfo,
                                                                                    Resource_type_id=resourcetype,
                                                                                    Resource_basecity=basecity,
                                                                                    Resource_brief=brief,
                                                                                    Resource_feature=feature,
                                                                                    Resource_value=value,
                                                                                    Resource_summary=summary, Data_owner_id=owner, Resource_code_id=resourcecode)
            else:
                # 生成 Resource 流水号
                Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(700, 799))
                #
                ResourceMaster.objects.create(Resource_image=imageurl,
                                            Resource_nickname=nickname,
                                            Resource_contactinfo=contactinfo,
                                            Resource_type_id=resourcetype,
                                            Resource_basecity=basecity,
                                            Resource_brief=brief,
                                            Resource_feature=feature,
                                            Resource_value=value,
                                            Resource_summary=summary,
                                            Data_owner_id=owner,
                                            on_webpage=onwebpage,
                                            Resource_code_id=resourcecode,
                                            Dummy_id=Dummy_id)
            #messages.info(request, '保存 sucess!')
            return redirect('/resourcelist/?user_dummy=' + request.user.Dummy_id)
        else:
            return render(request, 'resourcedetail.html', {'msg': resourcedetail_form.errors,'resourcedetail_form': resourcedetail_form, 'resource_dummy': resourcedummy,})
#
#服务列表
@login_required()
def service_list(request):
    _form_data = {}  # 回传参数
    _items = []  # 回传列表
    # 获取GET参数
    page = request.GET.get('page', 1)
    catalog = request.GET.get('catalog', 'all')
    resourcedummy = request.GET.get('resource_dummy', '')
    # 获取 User id
    jobresource = UserProfile.objects.get(Dummy_id=resourcedummy).defaultresource_id
    # 获取搜索框参数
    try:
        _filter = {}
        # 按钮条件筛选值
        if jobresource != '' and jobresource != 'all':
            _filter['Data_owner_id'] = jobresource
            if catalog == 'workshop':
                _filter['Job_type_id'] = 2
            else:
                if catalog == 'consulting':
                    _filter['Job_type_id'] = 1
        else:
            _filter['Data_owner_id'] = jobresource
        servicelist = JobMaster.objects.filter(**_filter).order_by("Data_id")
        _items = servicelist
        # --页码-- 获取URL中除page外的其它参数
        query_string = re.sub(r'page=[0-9]+[&]?', '', request.META.get('QUERY_STRING', None))
        if query_string:
            query_string = '&' + query_string
        _form_data['catalog'] = str(catalog)
        _form_data['resourcedummy'] = str(resourcedummy)

        paginator = Paginator(_items, 10)  # Show 20 contacts per page

        try:
            _items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            _items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            _items = paginator.page(paginator.num_pages)

        return render(request, "servicelist.html", {
            'form_data': _form_data,
            'servicelist': _items,
            'list': _items,
            'requestUrl': reverse('servicelist'),
            'query_string': query_string,
            'paginator': paginator,
        })
    except Exception as e:
        return HttpResponse('程序出错了！')
# 服务详情
@login_required()
def service_detail_edit(request):
    """用户资料维护"""
    job_dummy = request.GET.get('service_dummy', '')  # 用户 data id
    #
    if request.method == "GET":
        job_profile = JobMaster.objects.filter(Dummy_id=job_dummy)
        if job_profile:
            image = settings.MEDIA_URL + str(job_profile[0].Job_image)
            onwebpage = job_profile[0].on_webpage
            jobcode = job_profile[0].Job_code
            jobprice = job_profile[0].Job_price
            jobbrief = job_profile[0].Job_brief
            jobfeature = job_profile[0].Job_feature
            jobtarget = job_profile[0].Job_target
            jobdetail = job_profile[0].Job_detail
            #
            jobtype = job_profile[0].Job_type_id
            jobcontenttype = job_profile[0].Job_contenttype_id
            jobresource = job_profile[0].Job_resource_id
            owner = job_profile[0].Data_owner_id

            # 获取已有的数据，返回给前端页面
            servicedetail_form ={
                'mode': 'view',
                'nowuser': request.user.id,
                'job_dummy': job_dummy,
                'on_webpage': onwebpage,
                'imageurl': image,
                'job_code': jobcode,
                'job_price': jobprice,
                'job_brief': jobbrief,
                'job_feature': jobfeature,
                'job_target': jobtarget,
                'job_detail': jobdetail,
                #
                'job_type': jobtype,
                'job_contenttype': jobcontenttype,
                'job_resource': jobresource,
                'owner': owner,
            }
            #
            servicedetail_form = forms.ServiceForm(servicedetail_form) # 没有这句话不体现form定义的格式
            return render(request, 'servicedetail.html', {'msg': servicedetail_form.errors, 'servicedetail_form': servicedetail_form, 'job_dummy': job_dummy, 'imageurl': image})
        else:
            servicedetail_form = {
                'mode': 'edit',
                'nowuser': request.user.id,
                'job_dummy': '',
                'imageurl': '',
                'job_code': '',
                'job_price': '',
                'job_brief': '',
                'job_feature': '',
                'job_target': '',
                'job_detail': '',
                #
                'job_type': '',
                'job_contenttype': '',
                'job_resource': '',
                'owner': request.user.id,
            }
            servicedetail_form = forms.ServiceForm(servicedetail_form)
            return render(request,'servicedetail.html',{'msg':'请输入新增服务的内容','servicedetail_form': servicedetail_form, 'job_dummy': job_dummy})
    else:
        servicedetail_form = forms.ServiceForm(request.POST, request.FILES)
        if servicedetail_form.is_valid():# form验证通过
            # 获取页面数据保存到数据库
            imageurl = ''
            image = request.FILES.get('image', None)
            if image:
                # image resize
                imageTemproary = Image.open(image)
                outputIoStream = BytesIO()
                imageTemproaryResized = imageTemproary.resize((400, 320))
                imageTemproaryResized.save(outputIoStream, format='JPEG', quality=85)
                outputIoStream.seek(0)
                image = InMemoryUploadedFile(outputIoStream, 'ImageField',
                                             "%s.jpg" % image.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(outputIoStream), None)
                # image upload path
                currentYM = str(datetime.now().strftime('%Y%m'))
                upload_to = 'static/base/static/website/image/' + currentYM
                media_root = settings.MEDIA_ROOT
                full_path = media_root + '/' + upload_to
                if not os.path.exists(full_path):  # 判断路径是否存在
                    os.makedirs(full_path)  # 创建此路径
                # 上传图片文件
                with open(full_path + '/' + image.name, 'wb') as f:
                    for c in image.chunks():  # 相当于切片
                        f.write(c)
                #
                imageurl = upload_to + '/' + image.name
            #
            onwebpage = request.POST.get('on_webpage', None)
            jobcode = request.POST.get('job_code', None)
            jobprice = float(request.POST.get('job_price', None))
            jobbrief = request.POST.get('job_brief', None)
            jobfeature = request.POST.get('job_feature', None)
            jobtarget = request.POST.get('job_target', None)
            jobdetail = request.POST.get('job_detail', None)
            #
            jobtype = request.POST.get('job_type', None)
            jobcontenttype = request.POST.get('job_contenttype', None)
            jobresource = request.POST.get('job_resource', None)
            owner = int(request.POST.get('owner', None))
            #
            if onwebpage == 'on':
                onwebpage = True
            else:
                onwebpage = False
            #
            if JobMaster.objects.filter(Dummy_id=job_dummy):
                if image:
                    JobMaster.objects.filter(Dummy_id=job_dummy).update(Job_image=imageurl, Job_code=jobcode, on_webpage=onwebpage,
                                                                    Job_price=jobprice, Job_brief=jobbrief, Job_feature=jobfeature,
                                                                    Job_target=jobtarget, Job_detail=jobdetail, Job_type_id=jobtype,
                                                                   Job_contenttype_id=jobcontenttype, Data_owner_id=owner, Job_resource_id=jobresource)
                else:
                    JobMaster.objects.filter(Dummy_id=job_dummy).update(Job_code=jobcode, on_webpage=onwebpage,
                                                                   Job_price=jobprice, Job_brief=jobbrief,
                                                                   Job_feature=jobfeature,
                                                                   Job_target=jobtarget, Job_detail=jobdetail,
                                                                   Job_type_id=jobtype, Job_contenttype_id=jobcontenttype,
                                                                   Data_owner_id=owner, Job_resource_id=jobresource)
            else:
                # 生成 Service 流水号
                Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(800, 899))
                #
                JobMaster.objects.create(Job_image=imageurl, Job_code=jobcode,
                                       Job_price=jobprice, Job_brief=jobbrief,
                                       Job_feature=jobfeature, on_webpage=onwebpage,
                                       Job_target=jobtarget, Job_detail=jobdetail,
                                       Job_type_id=jobtype, Job_contenttype_id=jobcontenttype,
                                       Data_owner_id=owner, Job_resource_id=jobresource,
                                        Dummy_id=Dummy_id)
            #messages.info(request, '保存 sucess!')
            return redirect('/servicelist/?resource_dummy=' + request.user.Dummy_id)
        else:
            return render(request, 'servicedetail.html', {'msg': servicedetail_form.errors,'servicedetail_form': servicedetail_form, 'job_dummy': job_dummy,})
#
#request 列表
@login_required()
def request_list(request):
    _form_data = {}  # 回传参数
    _items = []# 回传列表
    # 获取GET参数
    page = request.GET.get('page', 1)
    catalog = request.GET.get('catalog','all')
    userdummy = request.GET.get('user_dummy', '0')
    # 获取搜索框参数
    try:
        _filter = {}
        # 按钮条件筛选值
        if userdummy != '':
            userid = UserProfile.objects.get(Dummy_id=userdummy).id
            _filter['Data_owner_id'] = userid
        if catalog == 'all':
            agendalist = RequestMaster.objects.filter(**_filter, Request_status__isnull=False).order_by("Data_id")
        else:
            agendalist = RequestMaster.objects.filter(**_filter, Request_usage=catalog, Request_status__isnull=False).order_by("Data_id")
        #
        _items = agendalist
        # --页码-- 获取URL中除page外的其它参数
        query_string = re.sub(r'page=[0-9]+[&]?', '', request.META.get('QUERY_STRING', None))
        if query_string:
            query_string = '&' + query_string

        _form_data['total'] = _items.count()
        _form_data['catalog'] = str(catalog)
        _form_data['userid'] = str(userid)
        _form_data['userdummy'] = userdummy

        paginator = Paginator(_items, 10)  # Show 20 contacts per page
        try:
            _items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            _items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            _items = paginator.page(paginator.num_pages)

        return render(request, "requestlist.html", {
            'form_data': _form_data,
            'requestlist': _items,
            'list': _items,
            'requestUrl': reverse('requestlist'),
            'query_string': query_string,
            'paginator': paginator,
        })
    except Exception as e:
        return HttpResponse('程序出错了！')
#request详情
@login_required()
def request_detail_edit(request):
    """用户资料维护"""
    dummy_id = request.GET.get('dummy_id', '')  # request dummy id
    #
    if request.method == "GET":
        request_profile = RequestMaster.objects.filter(Dummy_id=dummy_id)
        if request_profile:
            dataid = request_profile[0].Data_id
            dummyid = request_profile[0].Dummy_id
            desc = request_profile[0].Request_desc
            rdate = request_profile[0].Request_date
            initdate = request_profile[0].Request_initdate
            inittime = request_profile[0].Request_inittime
            enddate = request_profile[0].Request_enddate
            endtime = request_profile[0].Request_endtime
            comments = request_profile[0].Request_comments
            status = request_profile[0].Request_status
            #
            owner = request_profile[0].Data_owner_id
            approver = request_profile[0].Data_approver_id
            processor = request_profile[0].Data_processor_id
            realizer = request_profile[0].Data_realizer_id
            #
            resource = request_profile[0].Request_mainresource_id
            contact = request_profile[0].Request_contact_id
            customer = request_profile[0].Request_customer_id
            opportunity = request_profile[0].Request_opportunity_id
            # 获取已有的数据，返回给前端页面
            requestdetail_form ={
                'Data_id': dataid,
                'Dummy_id': dummyid,
                'Request_desc': desc,
                'Request_date': rdate,
                'Request_initdate': initdate,
                'Request_inittime': inittime,
                'Request_enddate': enddate,
                'Request_endtime': endtime,
                'Request_comments': comments,
                'Request_status': status,
                #
                'Data_owner': owner,
                'Data_approver': approver,
                'Data_processor': processor,
                'Data_realizer': realizer,
                #
                'Request_mainresource': resource,
                'Request_contact': contact,
                'Request_customer': customer,
                'Request_opportunity': opportunity,

            }
            #
            requestdetail_form = forms.RequestForm(requestdetail_form) # 没有这句话不体现form定义的格式
            return render(request, 'requestdetail.html', {'msg': requestdetail_form.errors, 'requestdetail_form': requestdetail_form, 'dummy_id': dummy_id})
        else:
            requestdetail_form = forms.RequestForm()
            return render(request,'requestdetail.html',{'msg':'请输入新增日程内容','requestdetail_form': requestdetail_form, 'dummy_id': dummy_id})
    else:
        requestdetail_form = forms.RequestForm(request.POST, request.FILES)
        if requestdetail_form.is_valid():# form验证通过
            # 获取页面数据保存到数据库
            status = request.POST.get('Request_status', None)
            #
            if RequestMaster.objects.filter(Data_id=request_id):
                RequestMaster.objects.filter(Data_id=request_id).update(Request_status=status)
            #messages.info(request, '更新 sucess!')
            return redirect('/requestlist/?userid=' + str(request.user.id)+'&catalog=' + 'all')
        else:
            return render(request, 'requestdetail.html', {'msg': requestdetail_form.errors,'requestdetail_form': requestdetail_form, 'request_id': request_id,})
#
#result 列表
@login_required()
def result_list(request):
    _form_data = {}  # 回传参数
    _items = []  # 回传列表
    # 获取GET参数
    page = request.GET.get('page', 1)
    catalog = request.GET.get('catalog', 'opportunity')
    userdummy = request.GET.get('user_dummy', '')  # 用户 userid
    # 获取搜索框参数
    try:
        _filter = {}
        # 按钮条件筛选值
        if userdummy != '':
            userid = UserProfile.objects.get(Dummy_id=userdummy).id
            _filter['Data_owner'] = userid
        if catalog == 'opportunity':
            resultlist = OpportunityMaster.objects.filter(**_filter).order_by("Data_id")
        elif catalog == 'contact':
            resultlist = ContactMaster.objects.filter(**_filter).order_by("Data_id")
        else:
            resultlist = CustomerMaster.objects.filter(**_filter).order_by("Data_id")
        #
        _items = resultlist
        # --页码-- 获取URL中除page外的其它参数
        query_string = re.sub(r'page=[0-9]+[&]?', '', request.META.get('QUERY_STRING', None))
        if query_string:
            query_string = '&' + query_string

        _form_data['total'] = _items.count()
        totalqty =0
        totalamt =0.00
        for item in _items:
            totalqty += int(1)
            totalamt += float(1.00)

        _form_data['totalqty'] = totalqty
        _form_data['totalamt'] = totalamt
        _form_data['catalog'] = catalog
        _form_data['userdummy'] = userdummy

        paginator = Paginator(_items, 10)  # Show 20 contacts per page

        try:
            _items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            _items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            _items = paginator.page(paginator.num_pages)

        return render(request, "resultlist.html", {
            'form_data': _form_data,
            'resultlist': _items,
            'list': _items,
            'requestUrl': reverse('resultlist'),
            'query_string': query_string,
            'paginator': paginator,
        })
    except Exception as e:
        return HttpResponse('程序出错了！')
#
#request详情
@login_required()
def contact_detail_edit(request):
    """用户资料维护"""
    contact_id = request.GET.get('data_id', 0)  # 用户 data id
    #
    if request.method == "GET":
        contact_profile = ContactMaster.objects.filter(Data_id=contact_id)
        if contact_profile:
            card = settings.MEDIA_URL + str(contact_profile[0].Contact_card)
            dataid = contact_profile[0].Data_id
            code = contact_profile[0].Contact_code
            name = contact_profile[0].Contact_name
            source = contact_profile[0].Contact_source
            method = contact_profile[0].Contact_method
            content = contact_profile[0].Contact_content
            flag = contact_profile[0].Contact_scanflag
            #
            owner = contact_profile[0].Data_owner_id
            creator = contact_profile[0].Data_creator_id
            status = contact_profile[0].Contact_status
            # 获取已有的数据，返回给前端页面
            contactdetail_form ={
                'mode': 'view',
                'nowuser': request.user.id,
                'Data_id': dataid,
                'Contact_code': code,
                'Contact_name': name,
                'Contact_source': source,
                'Contact_method': method,
                'Contact_content': content,
                'Contact_scanflag': flag,
                'Contact_status': status,
                #
                'Data_owner': owner,
                'Data_creator': creator,
            }
            #
            contactdetail_form = forms.ContactForm(contactdetail_form) # 没有这句话不体现form定义的格式
            return render(request, 'contactdetail.html', {'msg': contactdetail_form.errors, 'contactdetail_form': contactdetail_form, 'contact_id': contact_id, 'imageurl': card})
        else:
            contactdetail_form = {
                'mode': 'edit',
                'nowuser': request.user.id,
                'Data_id': '',
                'Contact_code': '',
                'Contact_name': '',
                'Contact_source': '',
                'Contact_method': '',
                'Contact_content': '',
                'Contact_scanflag': '',
                'Contact_status': '',
                #
                'Data_owner': request.user.id,
                'Data_creator': request.user.id,
            }
            contactdetail_form = forms.ContactForm(contactdetail_form)
            return render(request,'contactdetail.html',{'msg':'请输入新增联系人内容','contactdetail_form': contactdetail_form, 'contact_id': contact_id,})
    else:
        contactdetail_form = forms.ContactForm(request.POST, request.FILES)
        if contactdetail_form.is_valid():# form验证通过
            # 获取页面数据保存到数据库
            # 获取页面数据保存到数据库
            imageurl = ''
            image = request.FILES.get('Contact_card', None)
            if image:
                # image resize
                imageTemproary = Image.open(image)
                outputIoStream = BytesIO()
                imageTemproaryResized = imageTemproary.resize((400, 320))
                imageTemproaryResized.save(outputIoStream, format='JPEG', quality=85)
                outputIoStream.seek(0)
                image = InMemoryUploadedFile(outputIoStream, 'ImageField',
                                                               "%s.jpg" % image.name.split('.')[0],
                                                               'image/jpeg', sys.getsizeof(outputIoStream), None)
                # image upload path
                currentYM = str(datetime.now().strftime('%Y%m'))
                upload_to = 'static/base/static/website/image/' + currentYM
                media_root = settings.MEDIA_ROOT
                full_path = media_root + '/' + upload_to
                if not os.path.exists(full_path):  # 判断路径是否存在
                    os.makedirs(full_path)  # 创建此路径
                # 上传图片文件
                with open(full_path + '/' + image.name, 'wb') as f:
                    for c in image.chunks():  # 相当于切片
                        f.write(c)
                #
                imageurl = upload_to + '/' + image.name
            #
            code = request.POST.get('Contact_code', None)
            name = request.POST.get('Contact_name', None)
            source = request.POST.get('Contact_source', None)
            method = request.POST.get('Contact_method', None)
            content = request.POST.get('Contact_content', None)
            owner = int(request.POST.get('Data_owner', None))
            creator = int(request.POST.get('Data_creator', None))
            status = request.POST.get('Contact_status', None)
            #
            if ContactMaster.objects.filter(Data_id=contact_id):
                if image:
                    ContactMaster.objects.filter(Data_id=contact_id).update(Contact_card=imageurl, Contact_status=status)
                else:
                    ContactMaster.objects.filter(Data_id=contact_id).update(Contact_status=status)
            else:
                # 生成 Contact 流水号
                Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(200, 299))
                #
                up = UserProfile.objects.get(id=request.user.id)
                ContactMaster.objects.create(Contact_card=imageurl, Contact_code=code, Contact_name=name,
                                            Contact_source=source, Contact_method=method, Data_bu_id=up.Data_bu_id,
                                             Contact_content=content, Contact_status=status, Data_owner_id=owner,
                                             Data_creator_id=creator, Dummy_id=Dummy_id)
            #messages.info(request, '更新 sucess!')
            return redirect('/resultlist/?user_dummy=' + str(request.user.Dummy_id)+'&catalog=' + 'contact')
        else:
            return render(request, 'contactdetail.html', {'msg': contactdetail_form.errors,'contactdetail_form': contactdetail_form, 'contact_id': contact_id,})
#
#customer详情
@login_required()
def customer_detail_edit(request):
    """用户资料维护"""
    customer_id = request.GET.get('data_id', 0)  # 用户 data id
    #
    if request.method == "GET":
        customer_profile = CustomerMaster.objects.filter(Data_id=customer_id)
        if customer_profile:
            dataid = customer_profile[0].Data_id
            code = customer_profile[0].Customer_code
            name = customer_profile[0].Customer_name
            source = customer_profile[0].Customer_source
            address = customer_profile[0].Customer_address
            contact1 = customer_profile[0].Customer_contact1_id
            contact2 = customer_profile[0].Customer_contact2_id
            #
            owner = customer_profile[0].Data_owner_id
            creator = customer_profile[0].Data_creator_id
            status = customer_profile[0].Customer_status
            # 获取已有的数据，返回给前端页面
            customerdetail_form ={
                'mode': 'view',
                'nowuser': request.user.id,
                'Data_id': dataid,
                'Customer_code': code,
                'Customer_name': name,
                'Customer_source': source,
                'Customer_address': address,
                'Customer_contact1': contact1,
                'Customer_contact2': contact2,
                'Customer_status': status,
                #
                'Data_owner': owner,
                'Data_creator': creator,
            }
            #
            customerdetail_form = forms.CustomerForm(customerdetail_form) # 没有这句话不体现form定义的格式
            return render(request, 'customerdetail.html', {'msg': customerdetail_form.errors, 'customerdetail_form': customerdetail_form, 'customer_id': customer_id,})
        else:
            customerdetail_form = {
                'mode': 'edit',
                'nowuser': request.user.id,
                'Data_id': 0,
                'Customer_code': '',
                'Customer_name': '',
                'Customer_source': '',
                'Customer_address': '',
                'Customer_contact1': 0,
                'Customer_contact2': 0,
                'Customer_status': '',
                #
                'Data_owner': request.user.id,
                'Data_creator': request.user.id,
            }
            customerdetail_form = forms.CustomerForm(customerdetail_form)
            return render(request,'customerdetail.html',{'msg':'请输入新增客户内容','customerdetail_form': customerdetail_form, 'customer_id': customer_id,})
    else:
        customerdetail_form = forms.CustomerForm(request.POST, request.FILES)
        if customerdetail_form.is_valid():# form验证通过
            # 获取页面数据保存到数据库
            status = request.POST.get('Customer_status', None)
            #
            if CustomerMaster.objects.filter(Data_id=customer_id):
                CustomerMaster.objects.filter(Data_id=customer_id).update(Customer_status=status)
                #messages.info(request, '更新 sucess!')
            else:
                code = request.POST.get('Customer_code', None)
                name = request.POST.get('Customer_name', None)
                source = request.POST.get('Customer_source', None)
                address = request.POST.get('Customer_address', None)
                contact1 = request.POST.get('Customer_contact1', None)
                contact2 = request.POST.get('Customer_contact2', None)
                owner = request.POST.get('Data_owner', None)
                creator = request.POST.get('Data_creator', None)
                # 生成 Customer 流水号
                Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(300, 399))
                #
                up = UserProfile.objects.get(id=request.user.id)
                CustomerMaster.objects.create(Customer_code=code, Customer_name=name,
                                              Customer_source=source, Customer_address=address,
                                              Customer_contact1_id=contact1, Customer_contact2_id=contact2,
                                              Data_owner_id=owner, Data_creator_id=creator,
                                              Data_bu_id=up.Data_bu_id, Dummy_id=Dummy_id)
                #messages.info(request, '新增 sucess!')
            return redirect('/resultlist/?user_dummy=' + str(request.user.Dummy_id)+'&catalog=' + 'customer')
        else:
            return render(request, 'customerdetail.html', {'msg': customerdetail_form.errors,'customerdetail_form': customerdetail_form, 'customer_id': customer_id,})
#
#opportunity详情
@login_required()
def opportunity_detail_edit(request):
    """用户资料维护"""
    opportunity_id = request.GET.get('data_id', 0)  # 用户 data id
    #
    if request.method == "GET":
        opportunity_profile = OpportunityMaster.objects.filter(Data_id=opportunity_id)
        if opportunity_profile:
            dataid = opportunity_profile[0].Data_id
            code = opportunity_profile[0].Opportunity_code
            name = opportunity_profile[0].Opportunity_name
            source = opportunity_profile[0].Opportunity_source
            flowcycle = opportunity_profile[0].Opportunity_flowcycle_id
            initamt = opportunity_profile[0].Opportunity_initialamount
            nowamt = opportunity_profile[0].Opportunity_currentamount
            endamt = opportunity_profile[0].Opportunity_finalamount
            nowstage = opportunity_profile[0].Opportunity_nowstage
            nextstage = opportunity_profile[0].Opportunity_nextstage
            comments = opportunity_profile[0].Opportunity_comments
            #
            owner = opportunity_profile[0].Data_owner_id
            creator = opportunity_profile[0].Data_creator_id
            status = opportunity_profile[0].Opportunity_status
            # 获取已有的数据，返回给前端页面
            opportunitydetail_form ={
                'mode': 'view',
                'nowuser': request.user.id,
                'Data_id': dataid,
                'Opportunity_code': code,
                'Opportunity_name': name,
                'Opportunity_source': source,
                'Opportunity_flowcycle': flowcycle,
                'Opportunity_initialamount': str(initamt),
                'Opportunity_currentamount': str(nowamt),
                'Opportunity_finalamount': str(endamt),
                'Opportunity_nowstage': nowstage,
                'Opportunity_nextstage': nextstage,
                'Opportunity_comments': comments,
                'Opportunity_status': status,
                #
                'Data_owner': owner,
                'Data_creator': creator,
            }
            #
            opportunitydetail_form = forms.OpportunityForm(opportunitydetail_form) # 没有这句话不体现form定义的格式
            return render(request, 'opportunitydetail.html', {'msg': opportunitydetail_form.errors, 'opportunitydetail_form': opportunitydetail_form, 'opportunity_id': opportunity_id,})
        else:
            opportunitydetail_form = {
                'mode': 'edit',
                'nowuser': request.user.id,
                'Data_id': 0,
                'Opportunity_code': '',
                'Opportunity_name': '',
                'Opportunity_source': '',
                'Opportunity_flowcycle': '',
                'Opportunity_initialamount': '',
                'Opportunity_currentamount': '',
                'Opportunity_finalamount': '',
                'Opportunity_nowstage': '',
                'Opportunity_nextstage': '',
                'Opportunity_comments': '',
                'Opportunity_status': '',
                #
                'Data_owner': request.user.id,
                'Data_creator': request.user.id,
            }
            #
            opportunitydetail_form = forms.OpportunityForm(opportunitydetail_form)
            return render(request,'opportunitydetail.html',{'msg':'请输入新增商机内容', 'opportunitydetail_form': opportunitydetail_form, 'opportunity_id': opportunity_id,})
    else:
        opportunitydetail_form = forms.OpportunityForm(request.POST, request.FILES)
        if opportunitydetail_form.is_valid():# form验证通过
            # 获取页面数据保存到数据库
            status = request.POST.get('Opportunity_status', None)
            comments = request.POST.get('Opportunity_comments', None)
            #
            if OpportunityMaster.objects.filter(Data_id=opportunity_id):
                OpportunityMaster.objects.filter(Data_id=opportunity_id).update(Opportunity_status=status, Opportunity_comments=comments)
            else:
                code = request.POST.get('Opportunity_code', None)
                name = request.POST.get('Opportunity_name', None)
                source = request.POST.get('Opportunity_source', None)
                flowcycle = request.POST.get('Opportunity_flowcycle', None)
                initamt = request.POST.get('Opportunity_initialamount', None)
                contact = request.POST.get('Opportunity_contact', None)
                customer = request.POST.get('Opportunity_customer', None)
                owner = request.POST.get('Data_owner', None)
                creator = request.POST.get('Data_creator', None)
                # get owner's manager as approver
                up = UserProfile.objects.get(id=owner)
                approver = up.manager_id
                #
                # 生成 Opportunity 流水号
                Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(400, 499))
                #
                OpportunityMaster.objects.create(Opportunity_code=code, Opportunity_name=name, Opportunity_source=source, Data_bu_id=up.Data_bu_id,
                                                 Opportunity_flowcycle_id=flowcycle, Opportunity_initialamount=initamt, Opportunity_contact_id=contact,
                                                 Opportunity_customer_id=customer, Opportunity_ownershare=100.00, Data_owner_id=owner, Opportunity_comments=comments,
                                                 Data_creator_id=creator, Data_approver_id=approver, Opportunity_status='OPEN',
                                                 Dummy_id=Dummy_id)
            #messages.info(request, '更新 sucess!')
            return redirect('/resultlist/?user_dummy=' + str(request.user.Dummy_id)+'&catalog=' + 'opportunity')
        else:
            return render(request, 'opportunitydetail.html', {'msg': opportunitydetail_form.errors,'opportunitydetail_form': opportunitydetail_form, 'opportunity_id': opportunity_id,})
#
def view_funnel(request):
    pass
    return render(request,'view_funnel.html')
#
# 关注 操作
def love(request):
    #
    resource_id = request.GET.get('data_id', '')  # resource data id
    #
    #userid = UserProfile.objects.get(id=request.user.id).id
    if request.method == "GET":
        if UserInterest.objects.filter(User_interest_id=resource_id, User_myself_id=request.user.id, Data_status='00'):
            UserInterest.objects.filter(User_interest_id=resource_id, User_myself_id=request.user.id, Data_status='00').update(Data_datetime=datetime.now())
        else:
            if UserInterest.objects.filter(User_interest_id=resource_id, User_myself_id=request.user.id, Data_status='OK'):
                messages.info(request, '无需再次关注!')
            else:
                UserInterest.objects.create(Data_datetime=datetime.now(), User_interest_id=resource_id, User_myself_id=request.user.id, Data_status='00')
                messages.info(request, '关注 sucess! 等待通过。。。')
        return redirect('/resource/')
# 关注通过 操作
def lovepass(request):
    #
    resource_id = request.GET.get('resource_id', '')  # resource data id
    #
    if request.method == "GET":
        if UserInterest.objects.filter(User_interest_id=resource_id, Data_status='00'):
            UserInterest.objects.filter(User_interest_id=resource_id, Data_status='00').update(Data_datetime=datetime.now(), Data_status='OK')
            messages.info(request, '关注请求已通过!')
        else:
            messages.info(request, '无关注请求！')
        return redirect('/resourcelist/?user_dummy=' + request.user.Dummy_id)

# 点赞 操作
def thumpup(request):
    #
    resource_id = request.GET.get('data_id', '')  # resource data id
    #
    userid = UserProfile.objects.get(id=request.user.id).id
    if request.method == "GET":
        if UserThumbup.objects.filter(User_thumbup_id=resource_id, User_myself_id=request.user.id, Data_status='OK'):
            messages.info(request, '无需再次点赞!')
        else:
            UserThumbup.objects.create(Data_datetime=datetime.now(), User_thumbup_id=resource_id,
                                        User_myself_id=request.user.id, Data_status='OK')
            messages.info(request, '点赞 sucess!')
        return redirect('/resource/')
#