#
import xadmin
from crm.models import *
from base.models import *
from doc.models import *
from xadmin.layout import *
from django.utils.html import format_html
from django.http import HttpResponse
from django.core.validators import *
from django.core.validators import ValidationError
from django.contrib import messages
from django.shortcuts import render,redirect
from xadmin.views.base import get_account_bu  # psm add for get BU
# Register your models here.
class DocumentMasterAdmin(object):
    actions_on_top = True
    actions_selection_counter = None

    list_display = ('Data_bu', 'Document_code', 'Document_subject', 'colored_Document_type')
    exclude = ('')
    list_display_links = ('Document_code',)
    search_fields = ('Document_subject',)
    list_export_fields = ('Document_code', 'Document_subject', 'Document_type')
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    actions = ['test1', 'test2']
    model_icon = 'fa fa-book'
    save_as = False

    fields = ('Data_bu', 'Document_code', 'Document_subject', 'Document_body', 'Document_type', 'Document_attachment',
              'Document_version',
              'Data_owner', 'Data_creator', 'Data_approver', 'Data_security', 'Document_status',)
    readonly_fields = ('Document_status', 'Data_approver', 'Data_bu')
    form_layout = (
        Main(
            Fieldset('基本信息',
                     'Document_code', 'Document_subject', 'Document_type', 'Document_version'
                     ),
            Fieldset('正文信息',
                     'Document_body', 'Document_attachment',
                     ),
        ),
        Side(
            Fieldset('附加信息',
                     'Data_owner', 'Data_creator', 'Data_approver', 'Data_security', 'Document_status',
                     ),
        ),
    )

    def get_readonly_fields(self):
        if self.user.is_superuser or not self.org_obj:
            self.readonly_fields = []
        return self.readonly_fields

    # PSM add for default BU
    def instance_forms(self):
        super(DocumentMasterAdmin, self).instance_forms()
        if not self.org_obj:
            # PSM add for BU check
            if not self.user.is_superuser:
                account_bu = get_account_bu(self)
            else:
                account_bu = '*ALL'
            self.form_obj.initial['Data_bu_id'] = account_bu
            self.form_obj.initial['Data_bu'] = account_bu
            self.form_obj.initial['Data_owner'] = self.request.user.id
            self.form_obj.initial['Data_creator'] = self.request.user.id
        else:
            pass

    # PSM end for default BU
    # remove some auth  ---------
    def ResetAuth(self):
        # 重新定义此函数，限制普通用户的增删改权限
        if self.user.is_superuser:
            self.remove_permissions = ()
        return self.remove_permissions

    remove_permisson = ('delete',)

    # PSM add for Data filter by BU
    def queryset(self):
        qs = super(DocumentMasterAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu=account_bu)

    # 自定义屏幕列表字段
    def colored_Document_type(self, obj):
        color_code = ''
        if 'QT' == obj.Document_type:
            color_code = 'green'
        elif 'CT' == obj.Document_type:
            color_code = 'red'
        elif 'DF' == obj.Document_type:
            color_code = 'black'
        elif 'SL' == obj.Document_type:
            color_code = 'blue'
        elif 'OT' == obj.Document_type:
            color_code = 'pink'

        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            obj.Document_type,
        )

    colored_Document_type.short_description = u'来源'

xadmin.site.register(DocumentMaster, DocumentMasterAdmin)

class DocumentRelatedAdmin(object):
    actions_on_top = True
    actions_selection_counter = None

    list_display = ('Data_bu','Document_code', 'Document_subject','colored_Document_type')
    exclude = ('')
    list_display_links = ('Document_code',)
    search_fields = ('Document_subject',)
    list_export_fields = ('Document_code', 'Document_subject','Document_type')
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    actions = ['test1','test2']
    model_icon = 'fa fa-book'
    save_as = False

    fields = ('Document_code', 'Document_subject', 'Document_body', 'Document_type', 'Document_attachment', 'Document_version',
                     'Data_owner', 'Data_creator', 'Data_approver', 'Data_security', 'Document_status','DocRelated_Contact',
              'DocRelated_customer', 'DocRelated_opportunity', 'DocRelated_contract' ,'DocRelated_project')
    readonly_fields = ('Document_status', 'Data_approver')
    form_layout = (
        Main(
            Fieldset('基本信息',
                    'Document_code', 'Document_subject', 'Document_type', 'Document_version'
                     ),
            Fieldset('正文信息',
                     'Document_body','Document_attachment',
                     ),
            Fieldset('关联要素',
                     'DocRelated_Contact', 'DocRelated_customer', 'DocRelated_opportunity', 'DocRelated_contract', 'DocRelated_project',
                     ),
        ),
        Side(
            Fieldset('权属信息',
                      'Data_owner','Data_creator', 'Data_approver', 'Data_security', 'Document_status',
                     ),
        ),
    )
    def get_readonly_fields(self):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields
    # PSM add for default BU
    def instance_forms(self):
        super(DocumentRelatedAdmin, self).instance_forms()
        if not self.org_obj:
            # PSM add for BU check
            if not self.user.is_superuser:
                account_bu = get_account_bu(self)
            else:
                account_bu = '*ALL'
            self.form_obj.initial['Data_bu_id'] = account_bu
            self.form_obj.initial['Data_bu'] = account_bu
            self.form_obj.initial['Data_owner'] = self.request.user.id
            self.form_obj.initial['Data_creator'] = self.request.user.id
        else:
            pass
    # PSM end for default BU
# remove some auth  ---------
    def ResetAuth(self):
       # 重新定义此函数，限制普通用户的增删改权限
        if self.user.is_superuser:
            self.remove_permissions = ()
        return self.remove_permissions
    remove_permisson=('delete',)
    # PSM add for Data filter by BU
    def queryset(self):
        qs = super(DocumentRelatedAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu=account_bu)
    # 自定义屏幕列表字段
    def colored_Document_type(self, obj):
        color_code = ''
        if 'QT' == obj.Document_type:
            color_code = 'green'
        elif 'CT' == obj.Document_type:
            color_code = 'red'
        elif 'DF' == obj.Document_type:
            color_code = 'black'
        elif 'SL' == obj.Document_type:
            color_code = 'blue'
        elif 'OT' == obj.Document_type:
            color_code = 'pink'

        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            obj.Document_type,
        )

    colored_Document_type.short_description = u'来源'
#
xadmin.site.register(DocumentRelated, DocumentRelatedAdmin)
#
class ContentClassAdmin(object):
    actions_on_top = True
    actions_selection_counter = None

    list_display = ('Data_id','ContentClass_brief', 'ContentClass_user', 'is_pagetop')
    exclude = ('')
    list_display_links = ('ContentClass_brief',)
    search_fields = ('ContentClass_brief',)
    list_export_fields = ('ContentClass_brief', 'ContentClass_urlkey')
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-book'
    save_as = False

    fields = ('ContentClass_brief','ContentClass_urlkey','ContentClass_description','ContentClass_image','ContentClass_user','is_pagetop','Data_status',)

    form_layout = (
        Main(
            Fieldset('基本信息',
                    'ContentClass_brief','ContentClass_user',
                     ),
            Fieldset('正文信息',
                     'ContentClass_urlkey','ContentClass_description','ContentClass_image',
                     ),
        ),
        Side(
            Fieldset('other信息',
                     'is_pagetop',
                      'Data_status',
                     ),
        ),
    )
xadmin.site.register(ContentClass, ContentClassAdmin)
#
class ContentTypeAdmin(object):
    actions_on_top = True
    actions_selection_counter = None

    list_display = ('Data_id', 'ContentType_class', 'ContentType_brief', 'Content_shape','is_pagetop')
    exclude = ('')
    list_display_links = ('ContentType_brief',)
    search_fields = ('ContentType_brief',)
    list_export_fields = ('ContentType_brief', 'ContentType_urlkey')
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-book'
    save_as = False

    fields = ('ContentType_brief','ContentType_urlkey','ContentType_detail',
              'ContentType_class', 'ContentType_tag','ContentType_image','Content_shape','is_pagetop','Data_status')

    form_layout = (
        Main(
            Fieldset('基本信息',
                    'ContentType_tag','ContentType_class',
                     ),
            Fieldset('正文信息',
                     'ContentType_urlkey', 'ContentType_brief','ContentType_detail','ContentType_image',
                     ),
        ),
        Side(
            Fieldset('other信息',
                     'Content_shape', 'is_pagetop',
                      'Data_status',
                     ),
        ),
    )
xadmin.site.register(ContentType, ContentTypeAdmin)
#
# 基础能力
class BaseCompetenceAdmin(object):
    actions_on_top = True
    actions_selection_counter = None

    list_display = ('Data_id','BaseCompetence_type', 'BaseCompetence_timestart','BaseCompetence_timeend','BaseCompetence_quantity','is_active','Data_status')
    exclude = ('')
    list_display_links = ('Data_id',)
    search_fields = ('BaseCompetence_type',)
    list_export_fields = ('BaseCompetence_type', 'BaseCompetence_quantity')
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-book'
    save_as = False

    fields = ('BaseCompetence_type','BaseCompetence_timestart','BaseCompetence_timeend','BaseCompetence_quantity', 'is_active','Data_status')

    form_layout = (
        Main(
            Fieldset('基本信息',
                    'BaseCompetence_type',
                     ),
            Fieldset('正文信息',
                     'BaseCompetence_timestart','BaseCompetence_timeend','BaseCompetence_quantity',
                     ),
        ),
        Side(
            Fieldset('other信息',
                     'is_active',
                      'Data_status',
                     ),
        ),
    )
    #
    def formfield_for_dbfield(self, db_field, **kwargs):
       #
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'BaseCompetence_type':
            kwargs["queryset"] = ContentType.objects.filter(ContentType_class="RESOURCE")
        return db_field.formfield(**dict(**kwargs))
    #
xadmin.site.register(BaseCompetence, BaseCompetenceAdmin)
#  交付方式
class JobTypeAdmin(object):
    actions_on_top = True
    actions_selection_counter = None

    list_display = ('Data_id', 'JobType_code', 'JobType_content','is_pagetop')
    exclude = ('')
    list_display_links = ('Data_id',)
    search_fields = ('JobType_content',)
    list_export_fields = ('JobType_code', 'JobType_content')
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-book'
    save_as = False

    fields = ('JobType_code', 'JobType_content', 'JobType_detail', 'JobType_image','JobType_attachment','is_pagetop','Data_status',)

    form_layout = (
        Main(
            Fieldset('基本信息',
                     'JobType_code',
                     ),
            Fieldset('正文信息',
                     'JobType_content','JobType_detail','JobType_image','JobType_attachment',
                     ),
        ),
        Side(
            Fieldset('other信息',
                     'is_pagetop',
                     'Data_status',
                     ),
        ),
    )
xadmin.site.register(JobType, JobTypeAdmin)
#
class ResourceMasterAdmin(object):
    actions_on_top = True
    actions_selection_counter = None

    list_display = ('Data_id','Resource_type', 'Resource_code', 'Resource_nickname','is_pagetop', 'on_webpage')
    exclude = ('')
    list_display_links = ('Data_id',)
    search_fields = ('Resource_code',)
    list_export_fields = ('Resource_code', 'Resource_nickname')
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-book'
    save_as = False

    fields = ('Resource_code', 'Resource_nickname', 'Resource_type',
              'Resource_basicprice', 'Resource_image','Resource_attachment',
              'Resource_basecity', 'Resource_contactinfo', 'Resource_brief',
              'Resource_feature', 'Resource_value', 'Resource_summary','is_pagetop', 'on_webpage',
              'Data_status','Data_owner',
                      'Data_coordinator',)

    form_layout = (
        Main(
            Fieldset('基本信息',
                     'Resource_code', 'Resource_type',
                    'Resource_nickname','Resource_basecity','Resource_contactinfo',
                     ),
            Fieldset('正文信息',
                     'Resource_brief', 'Resource_feature','Resource_value','Resource_summary',
                      'Resource_basicprice','Resource_image','Resource_attachment',
                     ),
        ),
        Side(
            Fieldset('other信息',
                     'is_pagetop', 'on_webpage',
                     'Data_owner',
                     'Data_coordinator',
                     'Data_status',
                     ),
        ),
    )

xadmin.site.register(ResourceMaster, ResourceMasterAdmin)
#
class ResourceEditAdmin(object):
    actions_on_top = True
    actions_selection_counter = None

    list_display = ('Data_id','Resource_type', 'Resource_code', 'Resource_nickname','is_pagetop', 'on_webpage')
    exclude = ('')
    list_display_links = ('Data_id',)
    search_fields = ('Resource_code',)
    list_export_fields = ('Resource_code', 'Resource_nickname')
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-book'
    save_as = False
    hidden_menu = True

    fields = ('Resource_code', 'Resource_nickname', 'Resource_type',
              'Resource_basicprice', 'Resource_image','Resource_attachment',
              'Resource_basecity', 'Resource_contactinfo', 'Resource_brief',
              'Resource_feature', 'Resource_value', 'Resource_summary','is_pagetop', 'on_webpage',
              'Data_status','Data_owner',
                      'Data_coordinator',)

    form_layout = (
        Main(
            Fieldset('基本信息',
                     'Resource_code', 'Resource_type',
                    'Resource_nickname','Resource_basecity','Resource_contactinfo',
                     ),
            Fieldset('正文信息',
                     'Resource_brief', 'Resource_feature','Resource_value','Resource_summary',
                      'Resource_basicprice','Resource_image','Resource_attachment',
                     ),
        ),
        Side(
            Fieldset('other信息',
                     'is_pagetop', 'on_webpage',
                     'Data_owner',
                     'Data_coordinator',
                     'Data_status',
                     ),
        ),
    )

xadmin.site.register(ResourceEdit, ResourceEditAdmin)
#  资源能力
class ResourceCompetenceAdmin(object):
    actions_on_top = True
    actions_selection_counter = None

    list_display = ('Data_id', 'Resource_date', 'Resource_code','Resource_basecompetence','is_active')
    exclude = ('')
    list_display_links = ('Data_id',)
    search_fields = ('Resource_code',)
    list_export_fields = ('Resource_date', 'Resource_code',)
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-book'
    save_as = False

    fields = ('Resource_date', 'Resource_code','Resource_basecompetence','is_active','Data_status',)

    form_layout = (
        Main(
            Fieldset('基本信息',
                     'Resource_date',
                     ),
            Fieldset('正文信息',
                     'Resource_code','Resource_basecompetence',
                     ),
        ),
        Side(
            Fieldset('other信息',
                     'is_active',
                     'Data_status',
                     ),
        ),
    )
xadmin.site.register(ResourceCompetence, ResourceCompetenceAdmin)
#
class JobMasterAdmin(object):
    actions_on_top = True
    actions_selection_counter = None

    list_display = ('Data_id', 'Job_code', 'Job_contenttype','Job_resource','Job_type','is_pagetop', 'on_webpage')
    exclude = ('')
    list_display_links = ('Data_id',)
    search_fields = ('Job_code',)
    list_export_fields = ('Job_code', 'Job_resource', 'Job_type',)
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-book'
    save_as = False

    fields = ('Job_code', 'Job_code', 'Job_resource', 'Job_auxresource','Job_type',
              'Job_price', 'Job_image','Job_attachment','Job_contenttype',
              'Job_brief', 'Job_feature','Job_target',
              'Job_detail', 'is_pagetop',  'on_webpage', 'Data_status','Data_owner',
                      'Data_coordinator',)

    form_layout = (
        Main(
            Fieldset('基本信息',
                     'Job_code','Job_contenttype', 'Job_resource','Job_auxresource',
                     ),
            Fieldset('正文信息',
                     'Job_type','Job_price',
                     'Job_brief', 'Job_feature','Job_target',
                        'Job_detail',
                     'Job_image','Job_attachment',
                     ),
        ),
        Side(
            Fieldset('other信息',
                     'is_pagetop', 'on_webpage',
                     'Data_owner',
                      'Data_coordinator',
                      'Data_status',
                     ),
        ),
    )

xadmin.site.register(JobMaster, JobMasterAdmin)