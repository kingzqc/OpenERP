# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.core.validators import *
from django.core.validators import ValidationError
# below is PSM parameter setting
from base.psmsetting import *
from doc.models import *
from base.models import *
from random import randint
#  所有choices 参数来自于 psmsetting.py  =====
#
from django.contrib.auth.models import AbstractUser
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
# Create your models here.
class UserProfile(AbstractUser):

    gender_choices = (
        ('male','男'),
        ('female','女'),
        ('NA', '待定'),
    )
    resource_choices = (
        ('Trainer', '咨询授课'),
        ('Partner', '业务开拓'),
    )
    nick_name = models.CharField('昵称', max_length=32, default='')
    birthday = models.DateField('生日', null=True, blank=True)
    gender = models.CharField('性别',max_length=10,choices=gender_choices, default='NA')
    address = models.CharField('地址',max_length=100,default='')
    mobile = models.CharField('手机号',max_length=11,null=True,blank=True)
    image = models.ImageField(upload_to='static/base/static/%username/image/%Y%m',
                              default='static/base/static/image/default.png', max_length=200, null=True,blank=True)
    email = models.EmailField('邮箱',blank=True,unique=True) # 重写email，加上'唯一'标识 ，原因在于django中AbstractUser的email字段没设置唯一，容易造成多个用户邮箱相同
    usertype = models.CharField('用户类型', max_length=20, choices=resource_choices, default='Partner', null=True,blank=True)
    resourcetype = models.ForeignKey('doc.ContentType', verbose_name='资源类型', related_name='Content_type0',
                                      on_delete=models.CASCADE,
                                      blank=True, null=True)
    is_webuser = models.BooleanField(verbose_name='是否网页用户', default=False)
    Data_bu = models.ForeignKey("BUMaster", to_field='BU_code', verbose_name='所属BU',
                                related_name='BU_codeu', on_delete=models.CASCADE, null=True)
    manager = models.ForeignKey("UserProfile", verbose_name='上级', related_name='User_manager',
                                        on_delete=models.CASCADE, blank=True, null=True)
    defaultresource = models.ForeignKey(ResourceMaster, verbose_name='默认资源', related_name='dft_resource',
                                on_delete=models.CASCADE, blank=True, null=True)
    Dummy_id = models.CharField(verbose_name='流水号', max_length=20, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
    #
    def save(self, *args, **kwargs):
        # Dummy_id save
        if not self.Dummy_id:
            self.Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(900, 999))
        #
        super(UserProfile, self).save(*args, **kwargs)
#
# 关注信息表
class UserInterest(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    User_myself = models.ForeignKey(UserProfile, verbose_name='关注人', related_name='User_myself',
                                        on_delete=models.CASCADE, blank=True, null=True)
    User_interest = models.ForeignKey(ResourceMaster, verbose_name='关注对象', related_name='User_interest',
                                        on_delete=models.CASCADE, blank=True, null=True)
    Data_status = models.CharField(verbose_name='状态', max_length=2, default='OK',
                                      validators=[MinLengthValidator(1, message='20警示：')])
    Data_datetime = models.DateTimeField(verbose_name='日期', blank=True, null=True, auto_now_add=True)

    class Meta:
        unique_together = ('User_myself', 'User_interest')
        verbose_name = '关注'
        verbose_name_plural = '关注维护'

    def __str__(self):
        return str(self.Data_id)
#
# 点赞信息表
class UserThumbup(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    User_myself = models.ForeignKey(UserProfile, verbose_name='关注人', related_name='User_myself0',
                                        on_delete=models.CASCADE, blank=True, null=True)
    User_thumbup = models.ForeignKey(ResourceMaster, verbose_name='资源点赞', related_name='User_thumbup',
                                        on_delete=models.CASCADE, blank=True, null=True)
    Job_thumbup = models.ForeignKey(JobMaster, verbose_name='Job点赞', related_name='Job_thumbup',
                                        on_delete=models.CASCADE, blank=True, null=True)
    Data_status = models.CharField(verbose_name='状态', max_length=2, default='OK',
                                      validators=[MinLengthValidator(1, message='20警示：')])
    Data_datetime = models.DateTimeField(verbose_name='日期', blank=True, null=True, auto_now_add=True)

    class Meta:
        unique_together = ('User_myself', 'User_thumbup', 'Job_thumbup')
        verbose_name = '点赞'
        verbose_name_plural = '点赞维护'

    def __str__(self):
        return str(self.Data_id)
#
class EmailVerifyRecord(models.Model):
    """邮箱验证"""
    send_choices = (
        ('register','注册'),
        ('forget','找回密码'),
        ('update_email','修改邮箱')
    )

    code = models.CharField('验证码',max_length=10)
    email = models.EmailField('邮箱',max_length=50)
    send_type = models.CharField(choices=send_choices,max_length=30)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
#
class BUMaster(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    BU_code = models.CharField(verbose_name='BU代码', max_length=20, unique=True)
    BU_name = models.CharField(verbose_name='BU名称', max_length=60)
    BU_type = models.CharField(choices=base_BUTYPE, verbose_name='BU类型', max_length=60)
    BU_taxcode = models.CharField(verbose_name='BU税号', max_length=40, blank=True, null=True)
    BU_startdate = models.DateField(verbose_name='开始日期', default=datetime.now, blank=True, null=True)
    BU_expirydate = models.DateField(verbose_name='到期日期', null=True)
    BU_evidence = models.FileField(verbose_name='证明材料', max_length=200, blank=True, null=True)
    BU_status = models.CharField(choices=base_BUSTATUS,verbose_name='状态', max_length=2, default='OK',
                                 validators=[MinLengthValidator(1, message='20警示：')])
    BU_datetime = models.DateTimeField(verbose_name='日期', default=datetime.now, blank=True, null=True)
    BU_accounts = models.IntegerField(verbose_name='订购账户数', default=1)

    class Meta:
        verbose_name = '实体'
        verbose_name_plural = '经营实体'

    def __str__(self):
        return u'%s' % (self.BU_code,)

    def clean(self):
        # PSM add for 'check expiry'
        super(BUMaster, self).clean()
        if str(self.BU_expirydate) < str(self.BU_startdate):
            raise ValidationError({'BU_expirydate': '有效期晚于开始日期，请更正！'})
        if str(self.BU_expirydate) < timezone.now().strftime("%Y-%m-%d") and self.BU_status != 'XX':
            raise ValidationError({'BU_status': 'BU已经过期，状态有误！'})
# BU 参数
class BuParameter(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Bu_code = models.ForeignKey(BUMaster, to_field='BU_code', verbose_name='所属BU',
                                related_name='BU_name1', on_delete=models.CASCADE, blank=True, null=True)
    Bu_paratype = models.CharField(choices=base_PARATYPE, verbose_name='参数类型', max_length=10)
    Bu_parakey = models.CharField(verbose_name='参数值', max_length=10, blank=True, null=True)
    Bu_paravalue = models.CharField(verbose_name='参数名称', max_length=40, blank=True, null=True)
    Data_security = models.CharField(choices=base_SECURITYLEVEL, verbose_name='权限级别', max_length=10)

    class Meta:
        unique_together = ('Bu_code','Bu_paratype','Bu_parakey')
        verbose_name = '参数设置'
        verbose_name_plural = 'BU参数'
        ordering = ['Bu_code','Bu_paratype','Bu_parakey']

    def __str__(self):
        return str(self.Bu_paravalue)

# 服务内容
class ItemMaster(models.Model):
   #
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Data_bu = models.ForeignKey(BUMaster, to_field='BU_code', verbose_name='所属BU',
                                related_name='BU_namesi', on_delete=models.CASCADE, blank=True, null=True)
    Item_code = models.CharField(verbose_name='服务代码', max_length=20, blank=True, null=True)
    Item_desc = models.CharField(verbose_name='说明', max_length=200, blank=True, null=True)
    Item_unit = models.CharField(verbose_name='计量单位', max_length=10, blank=True, null=True)
    Item_baseprice = models.DecimalField(verbose_name='基础定价', max_digits=10, decimal_places=2, default=0.00)
    Data_creator = models.ForeignKey(UserProfile, verbose_name='创建者', related_name='Req_userim',
                                 on_delete=models.CASCADE, blank=True, null=True)
    Data_security = models.CharField(choices=base_SECURITYLEVEL, verbose_name='权限级别', max_length=10)
    Data_datetime = models.DateTimeField(verbose_name='日期', default=datetime.now, blank=True, null=True)
   #
    class Meta:
        unique_together = ('Data_bu','Item_code')
        verbose_name = '服务Item'
        verbose_name_plural = '服务Item'
        ordering = ['Data_bu','Item_code']

    def __str__(self):
        return str(self.Item_code)
# 自定义页面实现自己要的功能，不遵循XADMIN模板
class change_into(models.Model):

    class Meta:
        verbose_name = u"转入分析"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Meta.verbose_name
# 自定义页面实现自己要的功能，不遵循XADMIN模板
class change_out(models.Model):

    class Meta:
        verbose_name = u"转出分析"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Meta.verbose_name

