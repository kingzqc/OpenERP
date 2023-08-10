# 合同/项目的模型定义 
from django.db import models
from django.utils.html import format_html
from django.core.validators import *
from base.models import *
from crm.models import *
from doc.models import *
from workflow.models import *
from django.contrib.auth.models import User
from random import randint
#
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
# 合同主档
class ContractMaster(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Data_bu = models.ForeignKey('base.BUMaster', to_field='BU_code', verbose_name='所属BU', related_name='Data_bucctm', on_delete=models.CASCADE,
                                blank=True, null=True)
    Contract_code = models.CharField(verbose_name='合同代码', max_length=20)
    Contract_name = models.CharField(verbose_name='合同名称', max_length=200)
    Contract_customer = models.ForeignKey('crm.CustomerMaster', verbose_name='客户', related_name='Ct_cust1', on_delete=models.CASCADE,
                                blank=True, null=True)
    Contract_manager = models.ForeignKey('base.UserProfile', verbose_name='负责人', related_name='Ct_acct1', on_delete=models.CASCADE,
                                blank=True, null=True)
    Contract_method = models.CharField(choices=crm_METHOD, verbose_name='合同方式', max_length=10)
    Contract_content = models.TextField(verbose_name='合同内容', blank=True, null=True)
    Contract_document = models.ForeignKey('doc.DocumentMaster', verbose_name='相关文档', related_name='Ct_doc1', on_delete=models.CASCADE,
                                blank=True, null=True)
    Contract_amount = models.DecimalField(verbose_name='合同标的', max_digits=10, decimal_places=2, default=0.00)
    Contract_finishamount = models.DecimalField(verbose_name='完成金额', max_digits=10, decimal_places=2, default=0.00)
    Contract_updatedate = models.DateField(verbose_name='更新日期', blank=True, null=True)
    Contract_startdate = models.DateField(verbose_name='开始日期', blank=True, null=True)
    Contract_enddate = models.DateField(verbose_name='结束日期', blank=True, null=True)
    Contract_nowstage = models.CharField(verbose_name='当前进展', max_length=20, blank=True, null=True)
    Contract_nextstage = models.CharField(verbose_name='接续目标', max_length=20, blank=True, null=True)
    Contract_status = models.CharField(verbose_name='状态', max_length=2, default='OK', validators=[MinLengthValidator(1, message='20警示：')])
    Contract_comment = models.TextField(verbose_name='合同备注',  blank=True, null=True)
    #
    Data_security = models.CharField(choices=base_SECURITYLEVEL, verbose_name='权限级别', max_length=10)
    Data_owner = models.ForeignKey('base.UserProfile', verbose_name='拥有者', related_name='Ct_userdq', on_delete=models.CASCADE,
                                   blank=True, null=True)
    Data_secondowner = models.ForeignKey('base.UserProfile', verbose_name='第二拥有者', related_name='Ct_userds',
                                         on_delete=models.CASCADE,
                                         blank=True, null=True)
    Data_creator = models.ForeignKey('base.UserProfile', verbose_name='创建者', related_name='Ct_userdc', on_delete=models.CASCADE,
                                     blank=True, null=True)
    #
    Contract_initdate = models.DateField(verbose_name='建立日期', blank=True, null=True)
    Contract_changedate = models.DateField(verbose_name='修改日期', blank=True, null=True)
    Dummy_id = models.CharField(verbose_name='流水号', max_length=20, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = '合同'
    def __str__(self):
        return self.Contract_code
    #
    def save(self, *args, **kwargs):
        # Dummy_id save
        if not self.Dummy_id:
            self.Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(500, 599))
        #
        super(ContractMaster, self).save(*args, **kwargs)
    #
#自定义屏幕列表字段

# 合同资源
class ContractResourceMaster(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Data_bu = models.ForeignKey('base.BUMaster', to_field='BU_code', verbose_name='所属BU', related_name='Data_bucctr', on_delete=models.CASCADE,
                                blank=True, null=True)
    Contract_code = models.ForeignKey(ContractMaster, verbose_name='合同代码', related_name='cont_code0', on_delete=models.CASCADE, null=True)
    ContractResource_name = models.CharField(verbose_name='合同名称', max_length=20)
    ContractResource_role = models.CharField(choices=prj_ROLE, verbose_name='角色', max_length=12)
    ContractResource_member = models.CharField(verbose_name='资源', max_length=20)
    ContractResource_type = models.CharField(choices=prj_RESOURCETYPE, verbose_name='资源类型', max_length=10)
    ContractResource_unit = models.CharField(choices=prj_RESOURCEUNIT, verbose_name='资源单位', max_length=10)
    ContractResource_quantity = models.IntegerField(verbose_name='数量', default=0)
    ContractResource_amount = models.DecimalField(verbose_name='金额', max_digits=10, decimal_places=2, default=0.00)
    ContractResource_status = models.CharField(verbose_name='状态', max_length=2, default='OK',
                                       validators=[MinLengthValidator(1, message='20警示：')])
    ContractResource_comment = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)
    #
    Data_security = models.CharField(choices=base_SECURITYLEVEL, verbose_name='权限级别', max_length=10)

    class Meta:
        verbose_name = '合同资源'
        verbose_name_plural = '合同资源'
    def __str__(self):
        return self.ContractResource_name


# 项目主档
class ProjectMaster(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Data_bu = models.ForeignKey('base.BUMaster', verbose_name='所属BU', to_field='BU_code', related_name='Data_bucprj', on_delete=models.CASCADE,
                                blank=True, null=True)
    Project_parent = models.ForeignKey('ProjectMaster', verbose_name='上级项目', related_name='prj_prj1',
                                         on_delete=models.CASCADE,
                                         blank=True, null=True)
    Project_code = models.CharField(verbose_name='项目代码', max_length=20)
    Project_name = models.CharField(verbose_name='项目名称', max_length=200)
    Project_opportunity = models.ForeignKey('crm.OpportunityMaster', verbose_name='来自商机', related_name='prj_oppo1',
                                         on_delete=models.CASCADE,
                                         blank=True, null=True)
    Project_flowcycle = models.ForeignKey('workflow.FlowType', verbose_name='项目周期', related_name='Prj_cycle',
                                           on_delete=models.CASCADE, blank=True, null=True)
    Project_customer = models.ForeignKey('crm.CustomerMaster', verbose_name='客户', related_name='prj_cust1', on_delete=models.CASCADE,
                                blank=True, null=True)
    Project_manager = models.ForeignKey('base.UserProfile', verbose_name='项目经理', related_name='Cont_acct1', on_delete=models.CASCADE,
                                blank=True, null=True)
    Project_method = models.CharField(choices=crm_METHOD, verbose_name='项目方式', max_length=12)
    Project_serviceitem = models.ForeignKey('base.ItemMaster', verbose_name='服务内容', related_name='Pro_itemsi',
                                        on_delete=models.CASCADE, blank=True, null=True)
    Project_document = models.ForeignKey('doc.DocumentMaster', verbose_name='相关文档', related_name='prj_doc1',
                                          on_delete=models.CASCADE,
                                          blank=True, null=True)
    Project_amount = models.DecimalField(verbose_name='金额', max_digits=10, decimal_places=2, default=0.00)
    Project_quantity = models.DecimalField(verbose_name='服务数量', max_digits=10, decimal_places=1, default=0.0)
    Project_days = models.DecimalField(verbose_name='工作天数', max_digits=10, decimal_places=2, default=0.00)
    Project_realizeamount = models.DecimalField(verbose_name='已实现金额', max_digits=10, decimal_places=2, default=0.00)
    Project_processamount = models.DecimalField(verbose_name='已处理金额', max_digits=10, decimal_places=2, default=0.00)
    Project_realizeqty = models.DecimalField(verbose_name='已实现数量', max_digits=10, decimal_places=2, default=0.00)
    Project_realizedays = models.DecimalField(verbose_name='已实现天数', max_digits=10, decimal_places=1, default=0.0)
    Project_processqty = models.DecimalField(verbose_name='已处理数量', max_digits=10, decimal_places=2, default=0.00)
    Project_prcessdays = models.DecimalField(verbose_name='已处理天数', max_digits=10, decimal_places=1, default=0.0)
    Project_updatedate = models.DateField(verbose_name='更新日期', blank=True, null=True)
    Project_startdate = models.DateField(verbose_name='开始日期', blank=True, null=True)
    Project_enddate = models.DateField(verbose_name='结束日期', blank=True, null=True)
    Project_nowstage = models.CharField(verbose_name='当前进展', max_length=20, blank=True, null=True)
    Project_nextstage = models.CharField(verbose_name='接续目标', max_length=20, blank=True, null=True)
    Project_comment = models.TextField(verbose_name='备注', max_length=800, blank=True, null=True)
    #
    Data_security = models.CharField(choices=base_SECURITYLEVEL, verbose_name='权限级别', max_length=10)
    Data_owner = models.ForeignKey('base.UserProfile', verbose_name='拥有者', related_name='Prj_userdo', on_delete=models.CASCADE,
                                   blank=True, null=True)
    Data_secondowner = models.ForeignKey('base.UserProfile', verbose_name='第二拥有者', related_name='Prj_userds',
                                         on_delete=models.CASCADE,
                                         blank=True, null=True)
    Data_creator = models.ForeignKey('base.UserProfile', verbose_name='创建者', related_name='Prj_userdc', on_delete=models.CASCADE,
                                     blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='日期', default=datetime.now, blank=True, null=True)
    #
    Project_status = models.CharField(choices=prj_STATUS, verbose_name='状态', max_length=2, default='  ',
                                      validators=[MinLengthValidator(1, message='20警示：')])
    Dummy_id = models.CharField(verbose_name='流水号', max_length=20, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'

    def __str__(self):
        return self.Project_code
    #
    def save(self, *args, **kwargs):
        # Dummy_id save
        if not self.Dummy_id:
            self.Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(500, 599))
        #
        super(ProjectMaster, self).save(*args, **kwargs)
    #
# 项目批准
class ProjectResourceAssign(ProjectMaster):
    class Meta:
        verbose_name = '项目资源安排'
        verbose_name_plural = '项目资源安排'
        # 代理表 不产生新表
        proxy = True
# 项目批准
class ProjectApprove(ProjectMaster):
    class Meta:
        verbose_name = '项目批准'
        verbose_name_plural = '项目批准'
        # 代理表 不产生新表
        proxy = True
# 合同资源
class ProjectResourceMaster(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Data_bu = models.ForeignKey('base.BUMaster', verbose_name='所属BU', to_field='BU_code', related_name='Data_bucpr', on_delete=models.CASCADE,
                                blank=True, null=True)
    Project_code = models.ForeignKey(ProjectMaster, verbose_name='项目代码', related_name='prj_code1',
                                      on_delete=models.CASCADE, null=True)
    ProjectResource_name = models.CharField(verbose_name='项目资源名称', max_length=20, blank=True, null=True)
    ProjectResource_role = models.CharField(choices=prj_ROLE, verbose_name='角色', max_length=12, blank=True, null=True)
    ProjectResource_member = models.ForeignKey('base.UserProfile', verbose_name='成员', related_name='Prjr_usermbr',
                                   on_delete=models.CASCADE,
                                   blank=True, null=True)
    ProjectResource_type = models.CharField(choices=prj_RESOURCETYPE, verbose_name='资源类型', max_length=10, blank=True,
                                            null=True)
    ProjectResource_serviceitem = models.ForeignKey('base.ItemMaster', verbose_name='服务内容', related_name='Item_codepr',
                                            on_delete=models.CASCADE, blank=True, null=True)
    ProjectResource_unit = models.CharField(choices=prj_RESOURCEUNIT, verbose_name='资源单位', max_length=10, default='EA', blank=True, null=True)
    ProjectResource_quantity = models.DecimalField(verbose_name='数量', max_digits=10, decimal_places=1, default=0.0, blank=True, null=True)
    ProjectResource_price = models.DecimalField(verbose_name='金额', max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    ProjectResource_status = models.CharField(verbose_name='状态', max_length=2, default='OK',
                                      validators=[MinLengthValidator(1, message='20警示：')])
    ProjectResource_comment = models.TextField(verbose_name='备注', max_length=800, blank=True, null=True)
    #
    Data_security = models.CharField(choices=base_SECURITYLEVEL, verbose_name='权限级别', max_length=10)
    Data_owner = models.ForeignKey('base.UserProfile', verbose_name='拥有者', related_name='Prjr_userso',
                                   on_delete=models.CASCADE,
                                   blank=True, null=True)
    Data_creator = models.ForeignKey('base.UserProfile', verbose_name='创建者', related_name='Prjr_usersc',
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='日期', default=datetime.now, blank=True, null=True)

    class Meta:
        verbose_name = '项目资源'
        verbose_name_plural = '项目资源'

    def __str__(self):
        return self.ProjectResource_name
