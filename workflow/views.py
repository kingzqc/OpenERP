
from __future__ import unicode_literals
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
from workflow.models import *
from crm.models import *
from base.models import *
from django.contrib import messages
from random import randint
import logging
import datetime
'''
Dummy_id规则 后三位：
    workflow： （100-199）
    contact : (200-299)
    customer: (300-399)
    Opportunity: (400-499)
    Project: (500-599)
    Document:(600-699)
    Resource:(700-799)
    Service:(800-899)
    User:(900-999)
'''
# Create your views here.
#@login_required
#@permission_required('workflow.engine', login_url='/workflow/forbid/')
#@csrf_exempt
class workflow_engine:
    def __init__(self):
        self.message = 'fine'
    def FlowCycle_flow(self,flow_parameter):
        #
        wfmode = flow_parameter['mode']
        wfcycle = int(flow_parameter['cycle'])
        wfopportunity = int(flow_parameter['opportunity'])
        wfdatabuid = flow_parameter['databuid']
        wfresource = int(flow_parameter['resource'])
        wfcontact = int(flow_parameter['contact'])
        wfcustomer = int(flow_parameter['customer'])
        wfitem = int(flow_parameter['item'])
        wfstartdate = datetime.datetime.strptime(flow_parameter['startdate'], '%Y-%m-%d')
        wfproject = 1
        if flow_parameter['approver'] == 'None':
            wfapprover = 1
        else:
            wfapprover = int(flow_parameter['approver'])
        if flow_parameter['amount'] =='None':
            wfamount = 0.0
        else:
            wfamount = float(flow_parameter['amount'])
        #
        if wfmode == 'CREATEFLOW':
            # 获取 流程 用途
            fc = FlowType.objects.filter(Data_id=wfcycle).first()
            if fc:
                requestusage = fc.Flowtype_usage
            # 获取 流程周期 中的各个 request Type
            typelist = FlowCycleMaster.objects.filter(Flowcycle_type_id = wfcycle, Data_bu_id = wfdatabuid)
            #
            ### 提前产生所有request 的 dummy ID  start
            Dummy_id_list = []
            i = 0
            for type in typelist:
                if type.Flowcycle_stage_id != None and type.Flowcycle_stagedesc != None:
                    Dummy_id = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(((i*100)+100),((i*100)+199)))
                    Dummy_id_list.append(Dummy_id)
                i += 1
            ###  dummy ID   end
            # for workflow create start
            firstrequest = Dummy_id_list[0]
            nextrequest = ''
            i = 0
            for type in typelist:
                # 判断流程周期中有无定义，如果有才生成
                if type.Flowcycle_stage_id != None and type.Flowcycle_stagedesc != None:
                    #
                    if (i+1) < len(Dummy_id_list):
                        nextrequest = Dummy_id_list[i+1]
                    #
                    rt = RequestType.objects.filter(Data_id=type.Flowcycle_stage_id).first()
                    if rt:
                        # start date and end date  start  **** 默认是 按 8 小时 每天计算的天数
                        if (rt.Request_totaloverdue // 8) > 0:
                            requestduration = (rt.Request_totaloverdue % 8) + 1
                        else:
                            requestduration = (rt.Request_totaloverdue % 8)
                        wfenddate = wfstartdate + datetime.timedelta(days=requestduration)
                        # start date and end date  end
                        Data_approver = 1
                        Data_realizer = 1
                        Data_processor = 1
                        Data_reopener = 1
                        Data_backer = 1
                        print(str(rt.Request_approverrole),rt.Request_realizer,rt.Request_processor, rt.Request_reopener,rt.Request_backer)
                        if rt.Request_approver_id != None:
                            Data_approver = rt.Request_approver_id
                        else:
                            Data_approver = int(role_to_user(self, str(rt.Data_bu), str(rt.Request_approverrole), str(wfresource), str(wfcustomer), str(wfopportunity), str(wfproject)))
                        if rt.Request_realizer_id != None:
                            Data_realizer = rt.Request_realizer_id
                        else:
                            Data_realizer = int(role_to_user(str(rt.Data_bu), str(rt.Request_realizerrole), str(wfresource), str(wfcustomer), str(wfopportunity), str(wfproject)))
                        if rt.Request_processor_id != None:
                            Data_processor = rt.Request_processor_id
                        else:
                            Data_processor = int(role_to_user(str(rt.Data_bu), str(rt.Request_processorrole), str(wfresource), str(wfcustomer), str(wfopportunity), str(wfproject)))
                        if rt.Request_reopener_id != None:
                            Data_reopener = rt.Request_reopener_id
                        else:
                            Data_reopener = int(role_to_user(str(rt.Data_bu), str(rt.Request_reopenerrole), str(wfresource), str(wfcustomer), str(wfopportunity), str(wfproject)))
                        if rt.Request_backer_id != None:
                            Data_backer = rt.Request_backer_id
                        else:
                            Data_backer = int(role_to_user(str(rt.Data_bu), str(rt.Request_backerrole), str(wfresource), str(wfcustomer), str(wfopportunity), str(wfproject)))
                    # end if rt
                    #
                    wfobj = RequestMaster()
                    wfobj.Dummy_id = Dummy_id_list[i]
                    wfobj.Data_bu = rt.Data_bu
                    wfobj.Request_type_id = type.Flowcycle_stage_id
                    wfobj.Request_desc = type.Flowcycle_stagedesc
                    wfobj.Request_FlowCycle_id = wfcycle
                    wfobj.Request_usage = requestusage
                    wfobj.Request_opportunity_id = wfopportunity
                    wfobj.Request_account_id = wfresource
                    wfobj.Data_security = '10' # 自动生成的默认权限为 10
                    #  request person and role start
                    wfobj.Data_owner_id = wfresource
                    if wfapprover != 0:
                        wfobj.Data_approver_id = wfapprover
                    else:
                        wfobj.Data_approver_id = Data_approver
                    wfobj.Data_approverrole = rt.Request_approverrole
                    wfobj.Data_realizer_id = Data_realizer
                    wfobj.Data_realizerrole = rt.Request_realizerrole
                    wfobj.Data_processor_id = Data_processor
                    wfobj.Data_processorrole = rt.Request_processorrole
                    wfobj.Data_reopener_id = Data_reopener
                    wfobj.Data_reopenerrole = rt.Request_reopenerrole
                    wfobj.Data_backer_id = Data_backer
                    wfobj.Data_backerrole = rt.Request_backerrole
                    # request person and role end
                    wfobj.Request_contact_id = wfcontact
                    wfobj.Request_customer_id = wfcustomer
                    wfobj.Request_serviceitem_id = wfitem
                    wfobj.Request_amount = wfamount
                    wfobj.Request_initdate = wfstartdate
                    wfobj.Request_enddate = wfenddate
                    wfobj.Request_comments = '商机流程'
                    # 商机的第一个工作流是“待办”状态，后续都为空，暂时隐藏
                    if i == 0:
                        wfobj.Request_status = '00'
                    # 如果是最后一个 request， next request = ‘’
                    if nextrequest != Dummy_id_list[i]:
                        wfobj.Request_nextrequest = nextrequest
                    wfobj.save()
                # end if cycle*
                i += 1
                wfstartdate = wfenddate
            # for workflow create end
            self.message = str(wfcycle) + '工作流创建成功！'
        if wfmode == 'UPDATEFLOW':
            self.message = '工作流修改成功！'
        wf_para = {
            'message': self.message,
            'nowstage': firstrequest,
            'nextstage': nextrequest,
        }
        return wf_para
    def projectcycle_flow(self, flow_parameter):
        print('project function is under construction...')
    # *************************************
    #
# 此方法是把工作流类型中定义的各个角色转换为相应的用户   ******************************************************
'''self = 自己
    mgr = 上级
    accmgr = 客户经理
    oppmgr = 商机经理
    prjmgr = 项目经理'''
def role_to_user(self, databu='', rolecode='', wfresource='', wfcustomer='', wfopportunity=' ', wfproject=''):
    playerid = 1
    if rolecode == 'self':
        relatedata = int(wfresource)
        playerid = relatedata
    if rolecode == 'mgr':
        relatedata = int(wfresource)
        am = UserProfile.objects.filter(Data_bu_id=databu, id=relatedata).first()
        if am:
            playerid = am.manager_id
    if rolecode == 'accmgr':
        relatedata = int(wfcustomer)
        cm = CustomerMaster.objects.filter(Data_bu_id=databu, Data_id=relatedata).first()
        if cm:
            playerid = cm.Data_owner_id
    if rolecode == 'oppmgr':
        relatedata = int(wfopportunity)
        om = OpportunityMaster.objects.filter(Data_bu_id=databu, Data_id=relatedata).first()
        if om:
            playerid = om.Data_owner_id
    if rolecode == 'prjmgr':
        relatedata = int(wfproject)
        pm = ProjectMaster.objects.filter(Data_bu_id=databu, Data_id=relatedata).first()
        if pm:
            playerid = pm.Project_manager_id
    return str(playerid)