
# Create your models here.
from base.models import *
from ppm.models import *
from workflow.models import *
from doc.models import *
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from random import randint
from django.core.validators import *
from django.core.validators import ValidationError, MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
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
#
class ContactMaster(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Data_bu = models.ForeignKey(BUMaster, to_field='BU_code', verbose_name='所属BU', related_name='Data_buc1', on_delete=models.CASCADE, blank=True, null=True)
    Contact_code = models.CharField(verbose_name='联系人代码', max_length=10)
    Contact_name = models.CharField(verbose_name='联系人名称', max_length=20, blank=True, null=True)
    Contact_source = models.CharField(choices=crm_SOURCE, verbose_name='来源', max_length=60, blank=True, null=True)
    Contact_method = models.CharField(choices=crm_METHOD, verbose_name='联系方式', max_length=12, blank=True, null=True)
    Contact_content = models.TextField(verbose_name='联系内容', max_length=40, blank=True, null=True)
    Contact_card = models.ImageField(verbose_name='名片', blank=True, null=True)
    Contact_scanflag = models.CharField(choices=crm_SCANFLAG,verbose_name='识别标识', max_length=16, default='99', blank=True, null=True)
    Data_security = models.CharField(choices=base_SECURITYLEVEL, verbose_name='权限级别', max_length=10)
    Data_owner = models.ForeignKey(UserProfile, verbose_name='拥有者', related_name='User_nameco1', on_delete=models.CASCADE,blank=True, null=True)
    Data_creator = models.ForeignKey(UserProfile, verbose_name='创建者', related_name='User_namecc1', on_delete=models.CASCADE,blank=True, null=True)
    Contact_status = models.CharField(choices=crm_STATUS,verbose_name='状态', max_length=10, default='OPEN', validators=[MinLengthValidator(1, message='20警示：')])
    Contact_date = models.DateField(verbose_name='日期', blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='日期', default=datetime.now, blank=True, null=True)
    Dummy_id = models.CharField(verbose_name='流水号', max_length=20, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = '联系人'
        verbose_name_plural = '联系人'

    def __str__(self):
        return self.Contact_code
    #
    def save(self, *args, **kwargs):
        # Dummy_id save
        if not self.Dummy_id:
            self.Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(200, 299))
        #
        super(ContactMaster, self).save(*args, **kwargs)
    #
   # 屏幕字段内容校验
    def clean(self):
        super(ContactMaster, self).clean()
        # PSM add for 'check expiry'
        if str(self.Contact_card) == '' or self.Contact_scanflag == '99':
            if self.Contact_code is None:
                raise ValidationError({'Contact_code': '不能为空格！'})
            if self.Contact_name is None:
                raise ValidationError({'Contact_name': '不能为空格！'})
            if self.Contact_source is None:
                raise ValidationError({'Contact_source': '不能为空格！'})
            if self.Contact_method is None:
                raise ValidationError({'Contact_method': '不能为空格！'})
    # show name card image
    def show_image(self):
        return mark_safe('<img src="/medias/%s" height="30" width="60" />' % (self.Contact_card.url))

# Customer profile 客户信息表
class CustomerMaster(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Data_bu = models.ForeignKey(BUMaster, to_field='BU_code', verbose_name='所属BU', related_name='Data_buc0', on_delete=models.CASCADE,blank=True, null=True)
    Customer_code = models.CharField(verbose_name='客户代码', max_length=10)
    Customer_name = models.CharField(verbose_name='客户名称', max_length=20,blank=True, null=True)
    Customer_address = models.TextField(verbose_name='客户地址', max_length=200, blank=True, null=True)
    Customer_type = models.CharField(choices=crm_CUSTTYPE, verbose_name='类型', max_length=20, null=True)
    #
    Customer_source = models.CharField(choices=crm_SOURCE, verbose_name='来源', max_length=60, blank=True, null=True)
    Customer_industry = models.ForeignKey(BuParameter, verbose_name='行业', related_name='Ind_name', on_delete=models.CASCADE,blank=True, null=True)
    Customer_scale = models.ForeignKey(BuParameter, verbose_name='规模', related_name='Scal_name', on_delete=models.CASCADE,blank=True, null=True)
    Customer_service = models.ForeignKey(BuParameter, verbose_name='服务类型', related_name='Type_name', on_delete=models.CASCADE,blank=True, null=True)
    Customer_contact1 = models.ForeignKey(ContactMaster, verbose_name='联系人1', related_name='Cust_cont1', on_delete=models.CASCADE,blank=True, null=True)
    Customer_contact2 = models.ForeignKey(ContactMaster, verbose_name='联系人2', related_name='Cust_cont2',
                                          on_delete=models.CASCADE, blank=True, null=True)
    #
    Data_security = models.CharField(choices=base_SECURITYLEVEL, verbose_name='权限级别', max_length=10)
    Data_owner = models.ForeignKey(UserProfile, verbose_name='拥有者', related_name='Cust_userdo', on_delete=models.CASCADE,blank=True, null=True)
    Data_secondowner = models.ForeignKey(UserProfile, verbose_name='第二拥有者', related_name='Cust_userds',
                                         on_delete=models.CASCADE,
                                         blank=True, null=True)
    Data_creator = models.ForeignKey(UserProfile, verbose_name='创建者', related_name='Cust_userdc', on_delete=models.CASCADE,blank=True, null=True)
    Customer_status = models.CharField(choices=crm_STATUS,verbose_name='状态', max_length=10, default='OPEN', validators=[MinLengthValidator(1, message='20警示：')])
    Data_datetime = models.DateTimeField(verbose_name='日期', default=datetime.now, blank=True, null=True)
    Dummy_id = models.CharField(verbose_name='流水号', max_length=20, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = '客户'
        verbose_name_plural = '客户'

    def __str__(self):
        return self.Customer_code
    #
    def save(self, *args, **kwargs):
        # Dummy_id save
        if not self.Dummy_id:
            self.Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(300, 399))
        #
        super(CustomerMaster, self).save(*args, **kwargs)
    #
# Opportunity profile 商机信息表
class OpportunityMaster(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Data_bu = models.ForeignKey(BUMaster, to_field='BU_code', verbose_name='所属BU', related_name='Data_buo0', on_delete=models.CASCADE,
                                null=True)
    Opportunity_code = models.CharField(verbose_name='商机代码', max_length=20, null=True)
    Opportunity_name = models.CharField(verbose_name='商机名称', max_length=100, blank=True, null=True)
    #
    Opportunity_source = models.CharField(choices=crm_SOURCE, verbose_name='来源', max_length=10, null=True)
    Opportunity_flowcycle = models.ForeignKey('workflow.flowtype', verbose_name='销售周期', related_name='Opp_salscycle1', on_delete=models.CASCADE,
                                   null=True)
    Opportunity_contact = models.ForeignKey(ContactMaster, verbose_name='联系人', related_name='Opp_cont',
                                         on_delete=models.CASCADE,
                                         null=True)
    Opportunity_customer = models.ForeignKey(CustomerMaster, verbose_name='客户', related_name='Opp_cust',
                                          on_delete=models.CASCADE,
                                          null=True)
    Opportunity_initialamount = models.DecimalField(verbose_name='原始标的', max_digits=10, decimal_places=2, default=0.00)
    Opportunity_currentamount = models.DecimalField(verbose_name='当前标的', max_digits=10, decimal_places=2, default=0.00)
    Opportunity_finalamount = models.DecimalField(verbose_name='最终标的', max_digits=10, decimal_places=2, default=0.00)
    Opportunity_serviceitem = models.ForeignKey('base.ItemMaster', verbose_name='服务内容', related_name='Opp_item', on_delete=models.CASCADE,
                                   null=True)
    Opportunity_nowstage = models.CharField(verbose_name='当前进展', max_length=20, blank=True, null=True)
    Opportunity_nextstage = models.CharField(verbose_name='接续目标', max_length=20, blank=True, null=True)
    #
    Data_security = models.CharField(choices=base_SECURITYLEVEL, verbose_name='权限级别', max_length=10)
    Data_owner = models.ForeignKey(UserProfile, verbose_name='拥有者', related_name='Opp_userdo', on_delete=models.CASCADE,
                                   blank=True, null=True)
    Opportunity_ownershare = models.DecimalField(verbose_name='分担份额%', validators=[MinValueValidator(0.00),MaxValueValidator(100.00)], max_digits=6, decimal_places=2, default=0.00)
    Data_secondowner = models.ForeignKey(UserProfile, verbose_name='第二拥有者', related_name='Opp_userds', on_delete=models.CASCADE,
                                   blank=True, null=True)
    Opportunity_secondshare = models.DecimalField(verbose_name='分担份额%', validators=[MinValueValidator(0.00),MaxValueValidator(100.00)], max_digits=6, decimal_places=2, default=0.00)
    Data_creator = models.ForeignKey(UserProfile, verbose_name='创建者', related_name='Opp_userdc', on_delete=models.CASCADE,
                                     blank=True, null=True)
    Data_approver = models.ForeignKey(UserProfile, verbose_name='审批者', related_name='Opp_userda', on_delete=models.CASCADE,
                                     blank=True, null=True)
    Opportunity_status = models.CharField(choices=crm_STATUS, verbose_name='状态', max_length=10, default='OPEN',
                                       validators=[MinLengthValidator(1, message='20警示：')])
    Opportunity_date = models.DateField(verbose_name='商机日期', default=datetime.now, blank=True, null=True)
    Opportunity_comments = models.TextField(verbose_name='备注', max_length=800, blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='Data日期', default=datetime.now, blank=True, null=True)
    Dummy_id = models.CharField(verbose_name='流水号', max_length=20, blank=True, null=True, unique=True)

    class Meta:
        unique_together = ('Data_bu', 'Opportunity_code')
        ordering = ['Data_bu', 'Opportunity_code']
        verbose_name = '商机'
        verbose_name_plural = '商机'
    def __str__(self):
        return self.Opportunity_code

    # 屏幕字段内容校验
    def clean(self):
        super(OpportunityMaster, self).clean()
        # PSM add for 'check expiry'
        if str(self.Opportunity_nowstage) != 'None' and self.Opportunity_status == 'APPROVED':
            raise ValidationError({'Opportunity_status': '不能重复启用，请直接退出该商机！'})
        if str(self.Opportunity_nowstage) != 'None' and self.Opportunity_status == 'OPEN':
            raise ValidationError({'Opportunity_status': '已经启用的商机不能回退，请直接退出该商机！'})
        if str(self.Opportunity_status) == 'STOPPED' and self.Opportunity_status == 'OPEN':
            raise ValidationError({'Opportunity_status': '已经停用的商机不能再次启用，请直接退出该商机！'})
        if str(self.Opportunity_status) == 'APPROVED' and self.Opportunity_status == 'OPEN':
            raise ValidationError({'Opportunity_status': '已经批准的商机不能再次启用，请直接退出该商机！'})
        if (self.Opportunity_ownershare + self.Opportunity_secondshare) > 100.00:
            raise ValidationError({'Opportunity_secondshare': '比例总和大于100%，请修改！'})
        if (self.Opportunity_ownershare + self.Opportunity_secondshare) < 100.00 and (self.Opportunity_ownershare + self.Opportunity_secondshare) > 0:
            raise ValidationError({'Opportunity_secondshare': '比例总和不等于100%，请修改！'})
    #
    def save(self, *args, **kwargs):
        # Dummy_id save
        if not self.Dummy_id:
            self.Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(400, 499))
        #
        super(OpportunityMaster, self).save(*args, **kwargs)
    #
class OpportunityApprove(OpportunityMaster):
    class Meta:
        verbose_name = '商机批准'
        verbose_name_plural = '商机批准'
        # 代理表 不产生新表
        proxy = True
