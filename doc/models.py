from django.db import models
# Create your models here.
import sys
from base.models import *
from crm.models import *
from workflow.models import *
from ppm.models import *
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import *
from PIL import Image
from io import BytesIO
from random import randint
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import ValidationError
# Create your models here.
#  所有choices 参数来自于 psmsetting.py  =====
# Web内容分类信息表
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
class ContentClass(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Data_bu = models.ForeignKey('base.BUMaster', to_field='BU_code', verbose_name='所属BU', related_name='Data_budx',
                                on_delete=models.CASCADE,
                                blank=True, null=True)
    ContentClass_brief = models.CharField(choices=web_CONTENTCLASS,verbose_name='目录名', max_length=10, unique=True)
    ContentClass_urlkey = models.CharField(verbose_name='URL keywords', max_length=20)
    ContentClass_description = models.CharField(verbose_name='目录说明', max_length=200, blank=True, null=True)
    ContentClass_image = models.ImageField(verbose_name='图片资料(2560X300)', upload_to='static/base/static/website/image/%Y%m',
                                         default='static/base/static/image/default.png', blank=True, null=True)
    #
    ContentClass_user = models.ForeignKey('base.UserProfile', verbose_name='所属人', related_name='Resource_codecc',
                                      on_delete=models.CASCADE,
                                      blank=True, null=True)
    is_pagetop = models.BooleanField(verbose_name='是否页头展示', default=True)
    Data_status = models.CharField(verbose_name='状态', max_length=2, default='OK',
                                       validators=[MinLengthValidator(1, message='20警示：')])
    Data_changedate = models.DateField(verbose_name='修订日期', auto_now=timezone.now, blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='建立日期', default=datetime.now, blank=True, null=True)

    class Meta:
        verbose_name = '内容目录'
        verbose_name_plural = '内容目录维护'
    def __str__(self):
        return str(self.ContentClass_brief) + str(self.ContentClass_description)
    def save(self, *args, **kwargs):
        imageTemproary = Image.open(self.ContentClass_image)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((2560,300))
        imageTemproaryResized.save(outputIoStream , format='JPEG', quality=85)
        outputIoStream.seek(0)
        self.ContentClass_image = InMemoryUploadedFile(outputIoStream,'ImageField',"%s.jpg" %self.ContentClass_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        super(ContentClass, self).save(*args, **kwargs)
# 内容类型信息表
class ContentType(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    ContentType_brief = models.CharField(verbose_name='类型摘要', max_length=20)
    ContentType_class= models.ForeignKey(ContentClass, to_field='ContentClass_brief', verbose_name='所属目录', related_name='Content_class0',
                                on_delete=models.CASCADE,)
    ContentType_urlkey = models.CharField(verbose_name='类型URL', max_length=100, blank=True, null=True)
    ContentType_tag = models.CharField(verbose_name='标签', max_length=20, blank=True, null=True)
    ContentType_detail = models.TextField(verbose_name='详情', max_length=600, blank=True, null=True)
    #
    ContentType_image = models.ImageField(verbose_name='图片资料(400x320)',upload_to='static/base/static/website/image/%Y%m',
                              default='static/base/static/image/default.png', blank=True, null=True)
    ContentType_attachment = models.FileField(verbose_name='附件', upload_to='static/base/static/website/attachment/%Y%m',blank=True, null=True)
    #
    Content_shape = models.CharField(choices=web_RESOURCECLASS, verbose_name='内容形态',max_length=10, blank=True, null=True)
    is_pagetop = models.BooleanField(verbose_name='是否页头展示', default=False)
    Data_status = models.CharField(verbose_name='状态', max_length=2, default='OK',
                                       validators=[MinLengthValidator(1, message='20警示：')])
    Data_changedate = models.DateField(verbose_name='修订日期', auto_now=timezone.now, blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='建立日期', default=datetime.now, blank=True, null=True)

    class Meta:
        verbose_name = '内容类型'
        verbose_name_plural = '内容类型维护'
    def __str__(self):
        return str(self.ContentType_brief)
    def save(self, *args, **kwargs):
        imageTemproary = Image.open(self.ContentType_image)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((400,320))
        imageTemproaryResized.save(outputIoStream , format='JPEG', quality=85)
        outputIoStream.seek(0)
        self.ContentType_image = InMemoryUploadedFile(outputIoStream,'ImageField',"%s.jpg" %self.ContentType_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        super(ContentType, self).save(*args, **kwargs)
# 内容能力信息表
class BaseCompetence(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    BaseCompetence_type = models.ForeignKey('doc.ContentType', verbose_name='内容类型', related_name='Competence_type1',
                                      on_delete=models.CASCADE,
                                      blank=True, null=True)
    BaseCompetence_timestart = models.TimeField(verbose_name='开始时间', blank=True, null=True)
    BaseCompetence_timeend = models.TimeField(verbose_name='结束时间', blank=True, null=True)
    BaseCompetence_quantity = models.DecimalField(verbose_name='数量', max_digits=10, decimal_places=2, default=0.00)
    #
    is_active = models.BooleanField(verbose_name='是否可用', default=True)
    is_quantity = models.BooleanField(verbose_name='是否数量', default=False)
    #
    Data_status = models.CharField(verbose_name='状态', max_length=2, default='OK',
                                       validators=[MinLengthValidator(1, message='20警示：')])
    Data_changedate = models.DateField(verbose_name='修订日期', auto_now=timezone.now, blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='建立日期', default=datetime.now, blank=True, null=True)

    class Meta:
        verbose_name = '基础能力'
        verbose_name_plural = '基础能力维护'
    def __str__(self):
        return '['+ str(self.Data_id) +']'+ '[' + str(self.BaseCompetence_timestart) +']'+'---'+ '[' + str(self.BaseCompetence_timeend) + ']'
# 交付形式信息表
class JobType(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    JobType_code = models.CharField(verbose_name='交付方式', max_length=20)
    JobType_content = models.CharField(verbose_name='简要说明', max_length=200, blank=True, null=True)
    JobType_detail = models.TextField(verbose_name='详细说明', max_length=600, blank=True, null=True)
    #
    JobType_image = models.ImageField(verbose_name='图片资料(400x320)', upload_to='static/base/static/website/image/%Y%m',
                                         default='static/base/static/image/default.png', blank=True, null=True)
    JobType_attachment = models.FileField(verbose_name='附件', upload_to='static/base/static/website/attachment/%Y%m',
                                             blank=True, null=True)
    #
    is_pagetop = models.BooleanField(verbose_name='是否页头展示', default=False)
    Data_status = models.CharField(verbose_name='状态', max_length=2, default='OK',
                                       validators=[MinLengthValidator(1, message='20警示：')])
    Data_changedate = models.DateField(verbose_name='修订日期', auto_now=timezone.now, blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='建立日期', default=datetime.now, blank=True, null=True)

    class Meta:
        verbose_name = '交付方式'
        verbose_name_plural = '交付方式维护'
    def __str__(self):
        return str(self.JobType_content)
    def save(self, *args, **kwargs):
        imageTemproary = Image.open(self.JobType_image)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((400,320))
        imageTemproaryResized.save(outputIoStream , format='JPEG', quality=85)
        outputIoStream.seek(0)
        self.JobType_image = InMemoryUploadedFile(outputIoStream,'ImageField',"%s.jpg" %self.JobType_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        super(JobType, self).save(*args, **kwargs)
#
class ResourceMaster(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Resource_code = models.ForeignKey('base.UserProfile', verbose_name='相关人（可空）', related_name='Resource_codern',
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    Resource_type = models.ForeignKey('doc.ContentType', verbose_name='类型', related_name='Content_type1',
                                      on_delete=models.CASCADE,
                                      blank=True, null=True)
    Resource_nickname = models.CharField(verbose_name='资源标题', max_length=20, default='noname')
    Resource_basecity = models.CharField(verbose_name='所在城市', max_length=20, blank=True, null=True)
    Resource_contactinfo= models.CharField(verbose_name='联络信息', max_length=20, blank=True, null=True)
    Resource_brief = models.CharField(verbose_name='资源简介', max_length=200, blank=True, null=True)
    Resource_feature = models.TextField(verbose_name='资源特点', max_length=400, blank=True, null=True)
    Resource_value = models.TextField(verbose_name='资源价值', max_length=400, blank=True, null=True)
    Resource_summary = models.TextField(verbose_name='资源结论', max_length=400, blank=True, null=True)
    Resource_basicprice = models.DecimalField(verbose_name='参考价', max_digits=10, decimal_places=2, default=0.00,
                                        blank=True, null=True)
    #
    Resource_image = models.ImageField(verbose_name='图片资料(400x320)', upload_to='static/base/static/website/image/%Y%m',
                                             default='static/base/static/image/default.png', blank=True, null=True)
    Resource_attachment = models.FileField(verbose_name='附件',
                                                 upload_to='static/base/static/website/attachment/%Y%m',
                                                 blank=True, null=True)
    is_pagetop = models.BooleanField(verbose_name='是否页头展示', default=False)
    on_webpage = models.BooleanField(verbose_name='网页展示', default=False)
    Resource_recommendindex = models.IntegerField(verbose_name='推荐指数', default=0, blank=True, null=True)
    #
    Data_owner = models.ForeignKey('base.UserProfile', verbose_name='拥有者', related_name='Resc_userro', on_delete=models.CASCADE,blank=True, null=True)
    Data_coordinator = models.ForeignKey('base.UserProfile', verbose_name='协调人', related_name='Rescco_userro',
                                         on_delete=models.CASCADE,
                                         blank=True, null=True)
    Data_status = models.CharField(verbose_name='状态', max_length=2, default='OK',
                                   validators=[MinLengthValidator(1, message='20警示：')])
    Data_changedate = models.DateField(verbose_name='修订日期', auto_now=timezone.now, blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='建立日期', default=datetime.now, blank=True, null=True)
    Dummy_id = models.CharField(verbose_name='流水号', max_length=20, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = '资源'
        verbose_name_plural = '资源维护'

    def __str__(self):
        return  str(self.Data_id) + '/' + 'Owner:' +str(self.Data_owner)
    #
    def save(self, *args, **kwargs):
        # 上传图片时，resize
        imageTemproary = Image.open(self.Resource_image)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((400,320))
        imageTemproaryResized.save(outputIoStream, format='JPEG', quality=85)
        outputIoStream.seek(0)
        self.Resource_image = InMemoryUploadedFile(outputIoStream,'ImageField',"%s.jpg" %self.Resource_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        # Dummy_id save
        if not self.Dummy_id:
            self.Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(700, 799))
        #
        super(ResourceMaster, self).save(*args, **kwargs)
# 资源信息编辑
class ResourceEdit(ResourceMaster):
    class Meta:
        verbose_name = '编辑资料'
        verbose_name_plural = '编辑资料'
        # 代理表 不产生新表
        proxy = True
# 资源能力信息表
class ResourceCompetence(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Resource_date = models.DateField(verbose_name='能力日期', default=datetime.now, blank=True, null=True)
    Resource_code = models.ForeignKey('ResourceMaster', verbose_name='资源名', related_name='Resource_coderc',
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    Resource_basecompetence = models.ForeignKey('BaseCompetence', verbose_name='基础能力', related_name='Resource_competenceb',
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    is_active = models.BooleanField(verbose_name='是否可用', default=False)
    #
    Data_status = models.CharField(verbose_name='状态', max_length=2, default='OK',
                                   validators=[MinLengthValidator(1, message='20警示：')])
    Data_changedate = models.DateField(verbose_name='修订日期', auto_now=timezone.now, blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='建立日期', default=datetime.now, blank=True, null=True)

    class Meta:
        verbose_name = '资源能力'
        verbose_name_plural = '资源能力维护'

    def __str__(self):
        return str(self.Data_id)
# 讲师资质信息表
class JobMaster(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Job_code = models.CharField(verbose_name='服务名称', max_length=100, blank=True, null=True)
    Job_resource = models.ForeignKey('ResourceMaster', verbose_name='主要资源', related_name='Job_resource1', on_delete=models.CASCADE,
                                   blank=True, null=True)
    Job_auxresource = models.ForeignKey('ResourceMaster', verbose_name='辅助资源', related_name='Job_resource2', on_delete=models.CASCADE,
                                   blank=True, null=True)
    Job_contenttype = models.ForeignKey('doc.ContentType', verbose_name='内容类型', related_name='Job_conttype',
                                 on_delete=models.CASCADE,
                                 blank=True, null=True)
    Job_type = models.ForeignKey('doc.JobType', verbose_name='工作形式', related_name='JobType_code2',
                                           on_delete=models.CASCADE,
                                           blank=True, null=True)
    Job_price = models.DecimalField(verbose_name='Job参考价', max_digits=10, decimal_places=2, default=0.00,
                                                blank=True, null=True)
    #
    Job_brief = models.TextField(verbose_name='Job简介', max_length=100, blank=True, null=True)
    Job_feature = models.TextField(verbose_name='Job特色', max_length=200, blank=True, null=True)
    Job_target = models.TextField(verbose_name='Job目标', max_length=200, blank=True, null=True)
    Job_detail = models.TextField(verbose_name='Job大纲', max_length=1000, blank=True, null=True)
    Job_image = models.ImageField(verbose_name='图片资料(400x320)', upload_to='static/base/static/website/image/%Y%m',
                                             default='static/base/static/image/default.png', blank=True, null=True)
    Job_attachment = models.FileField(verbose_name='Job附件',
                                                 upload_to='static/base/static/website/attachment/%Y%m',
                                                 blank=True, null=True)
    #
    is_pagetop = models.BooleanField(verbose_name='是否页头展示', default=False)
    on_webpage = models.BooleanField(verbose_name='网页展示', default=False)
    Job_recommendindex = models.IntegerField(verbose_name='推荐指数', default=0, blank=True, null=True)
    #
    Data_owner = models.ForeignKey('base.UserProfile', verbose_name='拥有者', related_name='Job_userjo', on_delete=models.CASCADE,blank=True, null=True)
    Data_coordinator = models.ForeignKey('base.UserProfile', verbose_name='协调人', related_name='Jobco_userjo',
                                         on_delete=models.CASCADE,
                                         blank=True, null=True)
    Data_status = models.CharField(verbose_name='状态', max_length=2, default='OK',
                                       validators=[MinLengthValidator(1, message='20警示：')])
    Data_changedate = models.DateField(verbose_name='修订日期', auto_now=timezone.now, blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='建立日期', default=datetime.now, blank=True, null=True)
    Dummy_id = models.CharField(verbose_name='流水号', max_length=20, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = 'JOB'
        verbose_name_plural = '服务维护'
    def __str__(self):
        return str(self.Data_id) + str(self.Job_code)
    def save(self, *args, **kwargs):
        imageTemproary = Image.open(self.Job_image)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((400,320))
        imageTemproaryResized.save(outputIoStream , format='JPEG', quality=85)
        outputIoStream.seek(0)
        self.Job_image = InMemoryUploadedFile(outputIoStream,'ImageField',"%s.jpg" %self.Job_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        # Dummy_id save
        if not self.Dummy_id:
            self.Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(800, 899))
        #
        super(JobMaster, self).save(*args, **kwargs)
# Document profile 文档资料信息表
class DocumentMaster(models.Model):
    Data_id = models.AutoField(verbose_name='ID', primary_key=True)
    Data_bu = models.ForeignKey('base.BUMaster', to_field='BU_code',verbose_name='所属BU', related_name='Doc_bud0', on_delete=models.CASCADE,
                                blank=True, null=True)
    Document_code = models.CharField(verbose_name='文档代码', max_length=20)
    Document_version = models.CharField(verbose_name='文档版本', max_length=20, blank=True, null=True)
    Document_subject = models.CharField(verbose_name='文档标题', max_length=200, blank=True, null=True)
    Document_body = models.TextField(verbose_name='文档要点', blank=True, null=True)
    #
    Document_type = models.CharField(choices=doc_TYPE, verbose_name='类型', max_length=10, blank=True, null=True)
    Document_attachment = models.FileField(verbose_name='附件', blank=True, null=True)
    #
    Data_security = models.CharField(choices=base_SECURITYLEVEL, verbose_name='权限级别', max_length=10)
    Data_owner = models.ForeignKey('base.UserProfile', verbose_name='拥有者', related_name='Doc_namedo', on_delete=models.CASCADE,
                                   blank=True, null=True)
    Data_creator = models.ForeignKey('base.UserProfile', verbose_name='创建者', related_name='Doc_namedc', on_delete=models.CASCADE,
                                     blank=True, null=True)
    Data_approver = models.ForeignKey('base.UserProfile', verbose_name='审批人', related_name='Doc_nameda', on_delete=models.CASCADE,
                                     blank=True, null=True)
    #
    Document_status = models.CharField(verbose_name='状态', max_length=2, default='OK',
                                       validators=[MinLengthValidator(1, message='20警示：')])
    Document_initdate = models.DateField(verbose_name='创建日期', blank=True, null=True)
    Document_changedate = models.DateField(verbose_name='修订日期', auto_now=timezone.now, blank=True, null=True)
    Data_datetime = models.DateTimeField(verbose_name='日期', default=datetime.now, blank=True, null=True)
    Dummy_id = models.CharField(verbose_name='流水号', max_length=20, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = '文档'
        verbose_name_plural = '文档维护'
    def __str__(self):
        return self.Document_code
    #
    def save(self, *args, **kwargs):
        # Dummy_id save
        if not self.Dummy_id:
            self.Dummy_id = str(timezone.datetime.now().strftime('%Y%m%d%H%M%S')) + str(randint(600, 699))
        #
        super(DocumentMaster, self).save(*args, **kwargs)
class  DocumentRelated(DocumentMaster):
    #
    DocRelated_Contact = models.ForeignKey('crm.ContactMaster', verbose_name='相关联系人', related_name='Cont_namedr',
                                         on_delete=models.CASCADE,
                                         blank=True, null=True)
    DocRelated_customer = models.ForeignKey('crm.CustomerMaster', verbose_name='相关客户', related_name='Cust_namedr',
                                          on_delete=models.CASCADE,
                                          blank=True, null=True)
    DocRelated_request = models.ForeignKey('workflow.RequestMaster', verbose_name='相关活动', related_name='Act_namedr',
                                          on_delete=models.CASCADE,
                                          blank=True, null=True)
    DocRelated_opportunity = models.ForeignKey('crm.OpportunityMaster', verbose_name='相关商机', related_name='Opp_namedr',
                                             on_delete=models.CASCADE,
                                             blank=True, null=True)
    DocRelated_contract = models.ForeignKey('ppm.ContractMaster', verbose_name='相关合同', related_name='CT_namedr', on_delete=models.CASCADE,
                                          blank=True, null=True)
    DocRelated_project = models.ForeignKey('ppm.ProjectMaster', verbose_name='相关项目', related_name='Prj_namedr',
                                             on_delete=models.CASCADE,
                                             blank=True, null=True)
    #
    DocRelated_initdate = models.DateField(verbose_name='创建日期', blank=True, null=True)
    DocRelated_changedate = models.DateField(verbose_name='修订日期', auto_now=timezone.now, blank=True, null=True)

    class Meta:
        verbose_name = '相关文档'
        verbose_name_plural = '相关文档维护'