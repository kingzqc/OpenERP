import json
from base.models import *
from ppm.models import *
from crm.models import *
from doc.models import *
from django.utils.html import format_html
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from random import randint
from django.core.validators import *
from django.core.validators import ValidationError
from django.utils.safestring import mark_safe
from django import forms
# Create your models here.
#  所有choices 参数来自于 psmsetting.py  =====
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
# 工作流类型定义
class RequestCatalogue(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Data_bu = models.ForeignKey('base.BUMaster', to_field='BU_code', verbose_name='所属BU', related_name='Cat_namerc', on_delete=models.CASCADE, blank=True, null=True)
    Catalogue_code = models.CharField(verbose_name='目录代码', max_length=10, null=True)
    Catalogue_desc = models.CharField(verbose_name='目录说明', max_length=200, blank=True, null=True)
    Catalogue_type = models.CharField(choices=wf_MAINTYPE, verbose_name='目录类型', max_length=10)
    Catalogue_active = models.BooleanField(verbose_name='活跃', blank=True, null=True)
    Catalogue_comments = models.TextField(verbose_name='备注', max_length=400, blank=True)
    #
    Data_security = models.CharField(choices=base_SECURITYLEVEL, verbose_name='权限级别', max_length=10)
    Data_owner = models.ForeignKey('base.UserProfile', verbose_name='拥有者', related_name='Cat_userso',
                                   on_delete=models.CASCADE,
                                   blank=True, null=True)
    Data_creator = models.ForeignKey('base.UserProfile', verbose_name='创建者', related_name='Cat_usersc',
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='日期', default=datetime.now, blank=True, null=True)
    #
    class Meta:
        unique_together = ('Data_bu','Catalogue_code')
        verbose_name = '日程目录'
        verbose_name_plural = '日程目录'
        ordering = ['Data_bu','Catalogue_type','Catalogue_code']

    def __str__(self):
        return str(self.Catalogue_code)

# 工作流类型定义
class RequestType(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Data_bu = models.ForeignKey('base.BUMaster', to_field='BU_code', verbose_name='所属BU', related_name='Req_namert', on_delete=models.CASCADE, blank=True, null=True)
    RequestType_code = models.CharField(verbose_name='日程类型', max_length=20, null=True)
    RequestType_desc = models.CharField(verbose_name='类型说明', max_length=200, blank=True, null=True)
    # 日历 / CRM（漏斗） / 服务（项目实现）
    RequestType_catalogue = models.ForeignKey(RequestCatalogue, verbose_name='日程目录', related_name='Cat_coder', on_delete=models.CASCADE, null=True)
    # 流程内容必填与否设置
    Request_mustcont = models.BooleanField(verbose_name='联系必填', default=1,  null=True)
    Request_mustcust = models.BooleanField(verbose_name='客户必填', default=1,  null=True)
    Request_mustoppo = models.BooleanField(verbose_name='商机必填', default=1,  null=True)
    Request_mustproj = models.BooleanField(verbose_name='项目必填', default=1,  null=True)
    Request_mustdocu = models.BooleanField(verbose_name='文档必填', default=1,  null=True)
    Request_mustitem = models.BooleanField(verbose_name='服务必填', default=1,  null=True)
    # 具体人，或者角色
    Request_creator = models.ForeignKey('base.UserProfile', verbose_name='可创建人', related_name='Req_usercc',
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    Request_creatorrole = models.CharField(choices=wf_MAINROLE, verbose_name='可创建角色', max_length=20, blank=True, null=True)

    Request_approver = models.ForeignKey('base.UserProfile', verbose_name='可审批人', related_name='Req_userac',
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    Request_approverrole = models.CharField(choices=wf_MAINROLE, verbose_name='可审批角色', max_length=20, blank=True, null=True)
    Request_realizer = models.ForeignKey('base.UserProfile', verbose_name='可实现人', related_name='Req_userrc',
                                         on_delete=models.CASCADE,
                                         blank=True, null=True)
    Request_realizerrole = models.CharField(choices=wf_MAINROLE, verbose_name='可实现角色', max_length=20, blank=True,
                                            null=True)
    Request_processor = models.ForeignKey('base.UserProfile', verbose_name='可处理人', related_name='Req_userpc',
                                          on_delete=models.CASCADE,
                                          blank=True, null=True)
    Request_processorrole = models.CharField(choices=wf_MAINROLE, verbose_name='可处理角色', max_length=20, blank=True,
                                             null=True)
    Request_reopener = models.ForeignKey('base.UserProfile', verbose_name='可重开人', related_name='Req_userroc',
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    Request_reopenerrole = models.CharField(choices=wf_MAINROLE, verbose_name='可重开角色', max_length=20, blank=True, null=True)
    Request_backer = models.ForeignKey('base.UserProfile', verbose_name='可退回人', related_name='Req_userbc',
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    Request_backerrole = models.CharField(choices=wf_MAINROLE, verbose_name='可退回角色', max_length=20, blank=True, null=True)
    Request_deleter = models.ForeignKey('base.UserProfile', verbose_name='可删除人', related_name='Req_userdlc',
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    Request_deleterrole = models.CharField(choices=wf_MAINROLE, verbose_name='可删除角色', max_length=20, blank=True, null=True)
    # 默认 时长， 日程的计划参考
    Request_openoverdue = models.IntegerField(verbose_name='待办时长（小时）', default=8)
    Request_approveoverdue = models.IntegerField(verbose_name='审批时长（小时）', default=8)
    Request_realizeoverdue = models.IntegerField(verbose_name='实现时长（小时）', default=8)
    Request_totaloverdue = models.IntegerField(verbose_name='总共时长（小时）', default=24)
    #
    RequestType_active = models.BooleanField(verbose_name='停用（是/否）', blank=False, null=True)
    RequestType_comments = models.TextField(verbose_name='备注', max_length=800)
    #
    Data_security = models.CharField(choices=base_SECURITYLEVEL, verbose_name='权限级别', max_length=10)
    Data_owner = models.ForeignKey('base.UserProfile', verbose_name='拥有者', related_name='Req_usero',
                                   on_delete=models.CASCADE,
                                   blank=True, null=True)
    Data_creator = models.ForeignKey('base.UserProfile', verbose_name='创建者', related_name='Req_userc',
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='日期', default=datetime.now, blank=True, null=True)
    #
    class Meta:
        unique_together = ('Data_bu','RequestType_code')
        verbose_name = '日程类型'
        verbose_name_plural = '日程类型'
        ordering = ['Data_bu','RequestType_catalogue','RequestType_code']

    def __str__(self):
        return str(self.RequestType_code)
# 屏幕字段内容校验
    def clean(self):
        super(RequestType, self).clean()
        # PSM add for 'check expiry'
        errmsg = '角色和人不能同时为空，至少必须填一个！'
        errmsgsame = '审批人和创建人不能是同一个！'
        if str(self.Request_creatorrole) == 'None' and str(self.Request_creator) == 'None':
            raise ValidationError({'Request_creatorrole': errmsg})
        if (str(self.Request_approverrole) == 'None') and (str(self.Request_approver) == 'None'):
            raise ValidationError({'Request_approverrole': errmsg})
        if str(self.Request_realizerrole) == 'None' and str(self.Request_realizer) =='None':
            raise ValidationError({'Request_realizerrole': errmsg})
        if str(self.Request_processorrole) =='None' and str(self.Request_processor) =='None':
            raise ValidationError({'Request_processorrole': errmsg})
        if str(self.Request_reopenerrole) == 'None' and str(self.Request_reopener) == 'None':
            raise ValidationError({'Request_reopenerrole': errmsg})
        if str(self.Request_backerrole) == 'None' and str(self.Request_backer) == 'None':
            raise ValidationError({'Request_backerrole': errmsg})
        if str(self.Request_deleterrole) == 'None' and str(self.Request_deleter) == 'None':
            raise ValidationError({'Request_deleterrole': errmsg})
        #
        if str(self.Request_creator) == str(self.Request_approver) and str(self.Request_approver) != 'None':
            raise ValidationError({'Request_approver': errmsgsame})
# 流程类型
class FlowType(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Data_bu = models.ForeignKey('base.BUMaster', to_field='BU_code', verbose_name='所属BU', related_name='BU_nameft', on_delete=models.CASCADE, blank=True, null=True)
    Flowtype_code = models.CharField(choices=wf_CYCLETYPE,verbose_name='流程类型',max_length=10, default='STD', null=True)
    Flowtype_desc = models.CharField(verbose_name='说明', max_length=200, null=True)
    Flowtype_usage = models.CharField(choices=wf_CYCLEUSAGE, verbose_name='用途', max_length=10, default='C', null=True)
    Flowtype_active = models.BooleanField(verbose_name='活跃', default=0, blank=True, null=True)
    #
    Data_security = models.CharField(choices=base_SECURITYLEVEL, verbose_name='权限级别', max_length=10, blank=True, null=True)
    Data_owner = models.ForeignKey('base.UserProfile', verbose_name='拥有者', related_name='Flow_userso',
                                   on_delete=models.CASCADE, blank=True, null=True)
    Data_creator = models.ForeignKey('base.UserProfile', verbose_name='创建者', related_name='Flow_usersc',
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='日期', default=datetime.now, blank=True, null=True)
    class Meta:
        unique_together = ('Data_bu','Flowtype_code', 'Flowtype_usage')
        verbose_name = '流程类型'
        verbose_name_plural = '流程类型'
        ordering = ['Data_bu','Flowtype_code']

    def __str__(self):
        return format_html('{}'.format(str(self.Data_id)) + '--{}'.format(self.Flowtype_code) + '--{}'.format(self.Flowtype_desc))
# 销售周期
class FlowCycleMaster(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Data_bu = models.ForeignKey('base.BUMaster', to_field='BU_code', verbose_name='所属BU', related_name='BU_namefc', on_delete=models.CASCADE, blank=True, null=True)
    Flowcycle_type = models.ForeignKey(FlowType, verbose_name='流程类型', related_name='Flow_type',
                                          on_delete=models.CASCADE, blank=True, null=True)
   #
    Flowcycle_stagedesc = models.CharField(verbose_name='阶段说明', max_length=30, blank=True, null=True)
    Flowcycle_stage = models.ForeignKey(RequestType, verbose_name='阶段', related_name='Request_stage', on_delete=models.CASCADE, blank=True, null=True)
    #
    Data_security = models.CharField(choices=base_SECURITYLEVEL, verbose_name='权限级别', max_length=10)
    Data_owner = models.ForeignKey('base.UserProfile', verbose_name='拥有者', related_name='Flow_userfo',
                               on_delete=models.CASCADE,blank=True, null=True)
    Data_creator = models.ForeignKey('base.UserProfile', verbose_name='创建者', related_name='Flow_userfc',
                                 on_delete=models.CASCADE,
                                 blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='日期', default=datetime.now, blank=True, null=True)

    class Meta:
        verbose_name = '流程周期'
        verbose_name_plural = '流程周期'

    def __str__(self):
        return format_html('{}'.format(str(self.Data_id)))

# 工作流
class RequestMaster(models.Model):
   #
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Data_bu = models.ForeignKey('base.BUMaster', verbose_name='所属BU', to_field='BU_code', on_delete=models.CASCADE, blank=True, null=True)
    Dummy_id = models.CharField(verbose_name='流水号', max_length=20, blank=True, null=True, unique=True)
    Request_type = models.ForeignKey(RequestType, verbose_name='日程类型', related_name='Type_code', on_delete=models.CASCADE, blank=True, null=True)
    Request_desc = models.CharField(verbose_name='日程说明', max_length=200, blank=True, null=True)
    Request_cataloguetype = models.CharField(verbose_name='日程目录类型', max_length=20, blank=True, null=True)
    Request_account = models.ForeignKey('base.UserProfile', verbose_name='经办人', related_name='account_coder', on_delete=models.CASCADE, blank=True, null=True)
    Request_date = models.DateField(verbose_name='变更日期', blank=True, null=True)
    Request_duration = models.DecimalField(verbose_name='持续时间（小时）', max_digits=10, decimal_places=1, default=0.0)
    Request_initdate = models.DateField(verbose_name='开始日期',  blank=True, null=True)
    Request_inittime = models.TimeField(verbose_name='开始时间', blank=True, null=True)
    Request_enddate = models.DateField(verbose_name='结束日期',  blank=True, null=True)
    Request_endtime = models.TimeField(verbose_name='结束时间', blank=True, null=True)
    Request_actduration = models.DecimalField(verbose_name='实际持续时间（小时）', max_digits=10, decimal_places=1, default=0.0)
    Request_actinitdate = models.DateField(verbose_name='实际开始日期',  blank=True, null=True)
    Request_actinittime = models.TimeField(verbose_name='实际开始时间', blank=True, null=True)
    Request_actenddate = models.DateTimeField(verbose_name='实际结束日期', blank=True, null=True)
    Request_actendtime = models.DateTimeField(verbose_name='实际结束时间',  blank=True, null=True)
    #
    Request_customer = models.ForeignKey('crm.CustomerMaster', verbose_name='客户', related_name='Customer_coder', on_delete=models.CASCADE, blank=True, null=True)
    Request_contact = models.ForeignKey('crm.ContactMaster', verbose_name='联系人', related_name='Contact_coder',
                                         on_delete=models.CASCADE, blank=True, null=True)
    Request_opportunity = models.ForeignKey('crm.OpportunityMaster', verbose_name='商机', related_name='Opportunity_coder',
                                         on_delete=models.CASCADE, blank=True, null=True)
    Request_project = models.ForeignKey('ppm.ProjectMaster', verbose_name='项目', related_name='Prj_coder',
                                            on_delete=models.CASCADE, blank=True, null=True)
    Request_serviceitem = models.ForeignKey('base.ItemMaster', verbose_name='服务内容', related_name='Item_coder',
                                        on_delete=models.CASCADE, blank=True, null=True)
    Request_mainresource = models.ForeignKey('doc.ResourceMaster', verbose_name='主要资源', related_name='Main_resource0',
                                    on_delete=models.CASCADE, blank=True, null=True)
    Request_auxresource = models.ForeignKey('doc.ResourceMaster', verbose_name='辅助资源', related_name='Aux_resource0',
                                        on_delete=models.CASCADE, blank=True, null=True)

    Request_basecompetence = models.ForeignKey('doc.BaseCompetence', verbose_name='基础能力', related_name='Request_competenceb',
                                            on_delete=models.CASCADE,
                                            blank=True, null=True)
    Request_request = models.ForeignKey('RequestMaster', verbose_name='关联日程', to_field='Dummy_id', related_name='Request_coder',
                                            on_delete=models.CASCADE, blank=True, null=True)
    Request_flowcycle = models.ForeignKey('FlowType', verbose_name='销售周期', related_name='Request_cycle',
                                        on_delete=models.CASCADE, blank=True, null=True)
    Request_usage = models.CharField(choices=wf_CYCLEUSAGE, verbose_name='用途', max_length=10, default='', null=True)
    Request_nextrequest = models.CharField(verbose_name='接续日程', max_length=20, blank=True, null=True)
    #
    Request_quantity = models.DecimalField(verbose_name='数量', max_digits=10, decimal_places=2, default=0.00)
    Request_price = models.DecimalField(verbose_name='价格', max_digits=10, decimal_places=2, default=0.00)
    Request_amount = models.DecimalField(verbose_name='金额', max_digits=10, decimal_places=2, default=0.00)
    Request_actquantity = models.DecimalField(verbose_name='实际数量', max_digits=10, decimal_places=2, default=0.00)
    Request_actprice = models.DecimalField(verbose_name='实际价格', max_digits=10, decimal_places=2, default=0.00)
    Request_actamount = models.DecimalField(verbose_name='实际金额', max_digits=10, decimal_places=2, default=0.00)
    #
    Request_status = models.CharField(choices=wf_REQSTATUS, verbose_name='状态', max_length=2,
                                       validators=[MinLengthValidator(1, message='20警示：')], blank=True, null=True)
    Request_comments = models.TextField(verbose_name='备注', max_length=800)
    #
    Data_security = models.CharField(choices=base_SECURITYLEVEL, verbose_name='权限级别', max_length=10)
    Data_owner = models.ForeignKey('base.UserProfile', verbose_name='拥有者', related_name='Req_userso',
                                   on_delete=models.CASCADE,
                                   blank=True, null=True)
    Data_creator = models.ForeignKey('base.UserProfile', verbose_name='创建者', related_name='Req_usersc',
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    Data_creatorrole = models.CharField(choices=wf_MAINROLE, verbose_name='可创建角色', max_length=20, blank=True, null=True)
    Data_approver = models.ForeignKey('base.UserProfile', verbose_name='审批者', related_name='Req_usersa',
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    Data_approverrole = models.CharField(choices=wf_MAINROLE, verbose_name='可审批角色', max_length=20, blank=True, null=True)
    Data_realizer = models.ForeignKey('base.UserProfile', verbose_name='实现者', related_name='Req_userrr',
                                      on_delete=models.CASCADE,
                                      blank=True, null=True)
    Data_realizerrole = models.CharField(choices=wf_MAINROLE, verbose_name='可实现角色', max_length=20, blank=True, null=True)
    Data_processor = models.ForeignKey('base.UserProfile', verbose_name='处理者', related_name='Req_userpp',
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    Data_processorrole = models.CharField(choices=wf_MAINROLE, verbose_name='可处理角色', max_length=20, blank=True, null=True)
    Data_reopener = models.ForeignKey('base.UserProfile', verbose_name='处理者', related_name='Req_userrp',
                                       on_delete=models.CASCADE,
                                       blank=True, null=True)
    Data_reopenerrole = models.CharField(choices=wf_MAINROLE, verbose_name='可重开角色', max_length=20, blank=True, null=True)
    Data_backer = models.ForeignKey('base.UserProfile', verbose_name='退回者', related_name='Req_userbp',
                                       on_delete=models.CASCADE,
                                       blank=True, null=True)
    Data_backerrrole = models.CharField(choices=wf_MAINROLE, verbose_name='可退回角色', max_length=20, blank=True, null=True)
    Data_deleter = models.ForeignKey('base.UserProfile', verbose_name='删除者', related_name='Req_userdp',
                                       on_delete=models.CASCADE,
                                       blank=True, null=True)
    Data_deleterrole = models.CharField(choices=wf_MAINROLE, verbose_name='可删除角色', max_length=20, blank=True, null=True)
    Data_delegator = models.ForeignKey('base.UserProfile', verbose_name='代理者', related_name='Req_userdd',
                                       on_delete=models.CASCADE,
                                       blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='日期', blank=True, null=True)
    Request_isyes = models.BooleanField(verbose_name='是否执行', default=1, null=True)
    Request_cancel = models.BooleanField(verbose_name='取消(是/否)', default=0, null=True)

    class Meta:
        verbose_name = '工作流'
        verbose_name_plural = '工作流'
        ordering = ['Data_bu','Request_type']

    def __str__(self):
        return str(self.Dummy_id)
class RequestAction(models.Model):
   #
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Data_bu = models.ForeignKey('base.BUMaster', to_field='BU_code', verbose_name='所属BU', on_delete=models.CASCADE, blank=True, null=True)
    Request_id = models.ForeignKey(RequestMaster, verbose_name='日程ID', related_name='Action_reqid', on_delete=models.CASCADE, blank=True, null=True)
    #
    Request_action = models.CharField(choices=wf_ACTIONCODE, verbose_name='操作码', max_length=2, default='OO',
                                       validators=[MinLengthValidator(1, message='20警示：')])
    Action_player = models.ForeignKey('base.UserProfile', verbose_name='操作人', related_name='Action_user',
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    Action_datetime = models.DateTimeField(verbose_name='操作时间', default=datetime.now, blank=True, null=True)
    Request_comments = models.TextField(verbose_name='操作意见', max_length=400)
    class Meta:
        verbose_name = '工作流操作记录'
        verbose_name_plural = '工作流操作记录'
        ordering = ['Data_id','Request_id']

    def __str__(self):
        return str(self.Data_id)
# Request approve
class RequestApprove(RequestMaster):
    class Meta:
        verbose_name = '工作流批准'
        verbose_name_plural = '工作流批准'
        # 代理表 不产生新表
        proxy = True
# Request realize
class RequestRealize(RequestMaster):
    class Meta:
        verbose_name = '工作流实现'
        verbose_name_plural = '工作流实现'
        # 代理表 不产生新表
        proxy = True
# Request process
class RequestProcess(RequestMaster):
    class Meta:
        verbose_name = '工作流处理'
        verbose_name_plural = '工作流处理'
        # 代理表 不产生新表
        proxy = True
# Request reopen
class RequestReopen(RequestMaster):
    class Meta:
        verbose_name = '工作流重开'
        verbose_name_plural = '工作流重开'
        # 代理表 不产生新表
        proxy = True
# Request reopen
class RequestBackward(RequestMaster):
    class Meta:
        verbose_name = '工作流回退'
        verbose_name_plural = '工作流回退'
        # 代理表 不产生新表
        proxy = True
# Request pause
class RequestPause(RequestMaster):
    class Meta:
        verbose_name = '工作流暂停'
        verbose_name_plural = '工作流暂停'
        # 代理表 不产生新表
        proxy = True

