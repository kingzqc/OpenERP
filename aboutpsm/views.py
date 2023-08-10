from __future__ import unicode_literals
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from django.shortcuts import render,redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from base.models import *
from django.contrib import messages
import logging
from datetime import datetime,timedelta
from workflow.models import *
from crm.models import *
from django.db.models import Q
from django.db.models import Avg, Sum, Max, Min, Count
#
@login_required
#@permission_required('base.BU_VALID', login_url='/base/forbid/')
@csrf_exempt
# Create your views here.
def load_appoints(request):
    # 获取搜索框参数
    resource_id = int(request.GET.get('resource_id', '0'))
    month_firstday = request.GET.get('monthfirstday', '')
    month_lastday = request.GET.get('monthlastday', '')
    #
    start_date = datetime.strptime(month_firstday, '%Y-%m-%d')
    end_date = datetime.strptime(month_lastday, '%Y-%m-%d')
    #print(start_date, end_date, resource_id)
    try:
        data = {}
        idate = start_date
        request_date_list = []
        request_qty_list = []
        request_usage_list = []
        while idate <= end_date:
            request_date_list.append(datetime.strftime(idate,'%Y-%m-%d'))
            idate = idate + timedelta(days=1)
        #print(resource_id)
        if resource_id > 0:
            rmlist = RequestMaster.objects.filter((Q(Request_mainresource_id__exact=resource_id) | Q(Request_auxresource_id__exact=resource_id)),
                                                  Request_initdate__gte=start_date,
                                                  Request_initdate__lte=end_date, Request_status__gt='')
        else:
            rmlist = RequestMaster.objects.filter((Q(Data_owner_id__exact=request.user.id) | Q(Request_mainresource_id__exact=request.user.id) |
                                                   Q(Request_auxresource_id__exact=request.user.id)),
                                                  Request_initdate__gte=start_date,
                                                  Request_initdate__lte=end_date, Request_status__gt='')

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
        #
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
#==  获取 商机数据  ============
def load_opportunitys(request):
    # 获取搜索框参数
    from_date = request.GET.get('startdate', '')
    to_date = request.GET.get('enddate', '')
    data_range = request.GET.get('datarange', '')
    #
    start_date = datetime.strptime(from_date, '%Y-%m-%d')
    end_date = datetime.strptime(to_date, '%Y-%m-%d')
    #print(start_date, end_date)
    try:
        data = {}
        legend_list = []
        fedata_list = []
        fadata_list = []
        account_list = [] # 人员所属账号
        #
        if data_range == 'MYSELF':
            am = UserProfile.objects.filter(id=request.user.id).first()
            account_list.append(am.id)
        elif data_range == 'GROUP':
            amlist = UserProfile.objects.filter(manager_id=request.user.id)
            for am in amlist:
                account_list.append(am.id)
        elif data_range == 'COMPANY':
            am = UserProfile.objects.filter(id=request.user.id).first()
            amlist = UserProfile.objects.filter(Data_bu=am.Data_bu)
            for am in amlist:
                account_list.append(am.id)
        #print(account_list)
        flow_type = 2
        fclist = FlowCycleMaster.objects.filter(Flowcycle_type_id=flow_type, Data_bu_id=am.Data_bu)
        for fc in fclist:
            if fc.Flowcycle_stagedesc != None:
                legend_list.append(fc.Flowcycle_stagedesc)
        # 计算时间范围内的总金额， 用于计算百分比
        total = OpportunityMaster.objects.filter(Data_owner_id__in=account_list, Opportunity_date__gt=start_date, Opportunity_date__lte=end_date, Opportunity_flowcycle_id=flow_type).aggregate(total_expect=Sum('Opportunity_initialamount'), total_actual=Sum('Opportunity_currentamount'))
        #
        omlist = OpportunityMaster.objects.filter(Data_owner_id__in=account_list, Opportunity_date__gt=start_date,
                                                  Opportunity_date__lte=end_date,
                                                  Opportunity_flowcycle_id=flow_type)
        #print(legend_list)
        if omlist:
            code = '0'
            for legend in legend_list:
                feamount = 0.00
                faamount = 0.00
                fedata = {}
                fadata = {}
                for om in omlist:
                    # 汇总相同阶段的金额
                    rm = RequestMaster.objects.filter(Dummy_id=om.Opportunity_nowstage).first()
                    if rm:
                        if rm.Request_desc == legend:
                            feamount += float(om.Opportunity_initialamount)
                            faamount += float(om.Opportunity_currentamount)
            #
                fedata['value'] = int(feamount/float(total['total_expect'])*100)
                fedata['name'] = legend
                fedata_list.append(fedata)
                if feamount > 0:
                    fadata['value'] = int(float(faamount/feamount) * 100)
                    #fadata['value'] = 20
                else:
                    fadata['value'] = 0
                fadata['name'] = legend
                fadata_list.append(fadata)
            #
        else:
            code = '1'
            for legend in legend_list:
                feamount = 0.00
                fedata = {}
                faamount = 0.00
                fadata = {}
                #
                fedata['value'] = feamount
                fedata['name'] = legend
                fedata_list.append(fedata)
                fadata['value'] = faamount
                fadata['name'] = legend
                fadata_list.append(fedata)
        data = {
            "code": code,
            "legendlist": legend_list,
            "fedatalist": fedata_list,
            "fadatalist": fadata_list,
        }
        return JsonResponse(json.loads(json.dumps(data)))
    except Exception as e:
        return JsonResponse(code=-1, msg=u'获取商机失败', data=data)
#=========================================

