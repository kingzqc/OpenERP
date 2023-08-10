#
import xadmin
from crm.models import *
from base.models import *
from ppm.models import *
from workflow.models import *
from xadmin.layout import *
from django.contrib.admin.widgets import *
from django.utils.html import format_html
from django.http import HttpResponse
from django.core.validators import *
from django.core.validators import ValidationError
from django.contrib import messages
from django.shortcuts import render,redirect
from crispy_forms import *
from xadmin.views.base import get_account_bu  # psm add for get BU
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field, FormActions
# Register your models here.
# Project 项目
class ProjectResourceAssignInline(object):
    model = ProjectResourceMaster
    extra = 1
    style = 'table'
    fields = ['Project_code', 'ProjectResource_name', 'ProjectResource_role', 'ProjectResource_member',
              'ProjectResource_type', 'ProjectResource_serviceitem', 'ProjectResource_unit',
              'ProjectResource_quantity', 'ProjectResource_price', 'ProjectResource_status', 'ProjectResource_comment',
              'Data_security', 'Data_owner', 'Data_creator', 'Data_bu', 'Data_datetime',]
    exclude = ['Project_code', 'ProjectResource_status','ProjectResource_comment',
              'Data_security', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime',]
    readonly_fields = ()
    raw_id_fields = ['ProjectResource_member']

    def has_view_permission(self, request, obj=None):
        return False

class ResourceInlineFormset(forms.models.BaseInlineFormSet):
    # 页面字段内容的校验
    def clean(self):
        project = None
        resource = None
        if any(self.errors):
            return
        project = self.instance   # 取得的是项目code
        print(project)
        #if len(self.forms) < 1:
        #    raise forms.ValidationError(u'ProjectResource_member etetetetet', code='invalid')
        for f in self.forms:  # forms是inline的表格， f代表每一行内容
            name = f.cleaned_data.get('ProjectResource_name')
            item = f.cleaned_data.get('ProjectResource_serviceitem')
            qty = f.cleaned_data.get('ProjectResource_quantity')
            if name == None:
                raise forms.ValidationError(u'资源名称必须填入内容,请更正！', code='invalid')
            if item != None and qty<=0.0:
                raise forms.ValidationError((name +'行的数量错误，请更正！'), code='invalid')
            resource = f.save(commit=False)
        if project != None:
            print(project.Project_status)
            if project.Project_status in ['XX', 'OK']:
                raise forms.ValidationError((str(project) + u'状态不合适，不能修改资源内容，请直接退出！'), code='invalid')
class ProjectResourceInline(object):
    model = ProjectResourceMaster
    formset = ResourceInlineFormset
    extra = 1
    style = 'table'
    classes = ['collapse']
    fields = ['Project_code', 'ProjectResource_name', 'ProjectResource_role', 'ProjectResource_member',
              'ProjectResource_type', 'ProjectResource_serviceitem', 'ProjectResource_unit',
              'ProjectResource_quantity', 'ProjectResource_price', 'ProjectResource_status', 'ProjectResource_comment',
              'Data_security', 'Data_owner', 'Data_creator', 'Data_bu', 'Data_datetime',]
    exclude = ['Project_code', 'ProjectResource_status','ProjectResource_comment',
              'Data_security', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime',]
    readonly_fields = ()
    raw_id_fields = ['ProjectResource_member']



class ProjectMasterAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    prepopulated_fields = {'slug': ('Project_code',)}
    list_display = ('Project_code', 'Project_name','Project_parent', 'Project_status',)
    exclude = ('')
    list_display_links = ('Project_code',)
    search_fields = ('Project_code', 'Project_name')
    list_export_fields = ('Project_code', 'Project_name',)
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-check'
    save_as = False
    save = False
    remove_permissions = ('delete')
    show_bookmarks = False
    use_related_menu = False
    #
    fields = ['Project_parent','Project_code', 'Project_name', 'Project_customer',
              'Project_manager', 'Project_method', 'Project_opportunity',
              'Project_document','Project_amount','Project_quantity','Project_days','Project_comment','Project_flowcycle','Project_serviceitem',
              'Project_startdate','Project_enddate', 'Project_nowstage', 'Project_nextstage',
              'Data_security', 'Project_status', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime',]
    readonly_fields = ('Project_status', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime', )
    form_layout = (
        Main(
            Fieldset('基本信息',
                     Row('Project_parent', 'Project_code',),
                     'Project_name',
                     Row('Project_manager', 'Project_method', ),
                     ),
            Fieldset('关联要素信息',
                     Row('Project_customer','Project_document',),
                     Row('Project_flowcycle', 'Project_opportunity',),
                     css_class='unsort'
                     ),
            Fieldset('服务内容信息',
                     Row('Project_amount', 'Project_days', ),
                     Row('Project_startdate', 'Project_enddate', ),
                     Row('Project_serviceitem', 'Project_quantity', ),
                     Row('Project_nowstage', 'Project_nextstage', ),
                     css_class='unsort'
                     ),
        ),
        Side(
            Fieldset('审批信息',
                     'Project_status', 'Project_comment',
                     ),
            Fieldset('权属信息',
                      'Data_security', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime',
            ),
        ),
    )
    inlines = [ProjectResourceInline]
    #
    def ResetAuth(self):
        # 重新定义此函数，限制普通用户的增删改权限
        if self.user.is_superuser:
            self.remove_permissions = ()
        else:
            self.remove_permissions = ('delete', 'add',)
        return self.remove_permissions
    #
    def instance_forms(self):
        super().instance_forms()
        # 判断是否为新建操作
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
    # PSM end for default
    def get_readonly_fields(self):
        if not self.org_obj:  # 新建时
            readonly_fields = []
            return readonly_fields
        else:
            readonly_fields = ['Data_bu',]  # 修改时
            return readonly_fields
    def formfield_for_dbfield(self, db_field, **kwargs):
       #
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        account_bu = get_account_bu(self)
        if db_field.name == 'Project_serviceitem':
            kwargs["queryset"] = ItemMaster.objects.filter(Data_bu=account_bu)
        if db_field.name == 'Project_flowcycle':
            kwargs["queryset"] = FlowType.objects.filter(Data_bu=account_bu, Flowtype_usage ='P')
        return db_field.formfield(**dict(**kwargs))
    #
# PSM add for Data filter by BU
    def queryset(self):
        qs = super(ProjectMasterAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu=account_bu)
    #
    def save_models(self):
        obj = self.new_obj
        #
        if not obj.Project_name:
            obj.Project_name = obj.Project_code
            obj.save()
        else:
            super(ProjectMasterAdmin, self).save_models()

xadmin.site.register(ProjectMaster, ProjectMasterAdmin)
class ProjectResourceAssignAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    prepopulated_fields = {'slug': ('Project_code',)}
    list_display = ('Project_code', 'Project_name','Data_bu','Project_status',)
    exclude = ('')
    list_display_links = ('Project_code',)
    search_fields = ('Project_code', 'Project_name')
    list_export_fields = ('Project_code', 'Project_name',)
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-check'
    save_as = False
    save = False
    remove_permissions = ('delete')
    show_bookmarks = False
    use_related_menu = False
    #
    fields = ['Project_code', 'Project_name', 'Project_customer',
              'Project_manager', 'Project_method', 'Project_opportunity',
              'Project_document','Project_amount','Project_quantity','Project_days','Project_comment','Project_flowcycle','Project_serviceitem',
              'Project_startdate','Project_enddate',
              'Data_security', 'Project_status', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime',]
    readonly_fields = ('Project_status', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime', )
    inlines = [ProjectResourceAssignInline]
    form_layout = (
        Main(
            Fieldset('基本信息',
                     Row('Project_name', 'Project_code',),
                     Row('Project_manager', 'Project_method', ),
                     ),
            Fieldset('关联要素信息',
                     Row('Project_customer','Project_document',),
                     Row('Project_flowcycle', 'Project_opportunity',),
                     css_class='unsort'
                     ),
            Fieldset('服务内容信息',
                     Row('Project_amount', 'Project_days', ),
                     Row('Project_startdate', 'Project_enddate', ),
                     Row('Project_serviceitem', 'Project_quantity', ),
                     css_class='unsort'
                     ),
        ),
        Side(
            Fieldset('审批信息',
                     'Project_status', 'Project_comment',
                     ),
            Fieldset('权属信息',
                      'Data_security', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime',
            ),
        ),
    )
#
    def instance_forms(self):
        super().instance_forms()
        # 判断是否为新建操作
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
    # PSM end for default
    def get_readonly_fields(self):
        if not self.org_obj:  # 新建时
            readonly_fields = []
            return readonly_fields
        else:
            readonly_fields = ['Project_code', 'Project_name', 'Project_customer',
              'Project_manager', 'Project_method', 'Project_opportunity',
              'Project_document','Project_amount','Project_quantity','Project_days','Project_comment','Project_flowcycle','Project_serviceitem',
              'Project_startdate','Project_enddate',
              'Data_security', 'Project_status', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime',] # 修改时
            return readonly_fields
    def formfield_for_dbfield(self, db_field, **kwargs):
       #
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        account_bu = get_account_bu(self)
        if db_field.name == 'Project_serviceitem':
            kwargs["queryset"] = ItemMaster.objects.filter(Data_bu=account_bu)
        if db_field.name == 'Project_flowcycle':
            kwargs["queryset"] = FlowType.objects.filter(Data_bu=account_bu, Flowtype_usage ='P')
        return db_field.formfield(**dict(**kwargs))
    #
# PSM add for Data filter by BU
    def queryset(self):
        qs = super(ProjectResourceAssignAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu=account_bu)
    #
    def save_related(self):
        obj = self.new_obj
        #
        for formset in self.formsets:
            pass
        obj.save()
        super(ProjectResourceAssignAdmin, self).save_related()
        prms = ProjectResourceMaster.objects.filter(Project_code_id = formset.instance.Data_id)
        for prm in prms:
            prm.Project_code_id = formset.instance.Data_id
            prm.Data_bu = formset.instance.Data_bu
            prm.Data_creator = formset.instance.Data_creator
            prm.Data_owner = formset.instance.Data_owner

            prm.save()

    def save_models(self):
        obj = self.new_obj
        if not obj.Project_name:
            obj.Project_name = obj.Project_code
            obj.save()
        else:
            super(ProjectResourceAssignAdmin, self).save_models()

xadmin.site.register(ProjectResourceAssign, ProjectResourceAssignAdmin)
# Project 项目资源
class ProjectResourceAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    prepopulated_fields = {'slug': ('Project_code',)}
    list_display = ('Project_code', 'ProjectResource_name', 'ProjectResource_member', 'ProjectResource_serviceitem',)
    exclude = ('')
    list_display_links = ('Project_code',)
    list_filter = ['Project_code']
    search_fields = ('Project_code', 'ProjectResource_name')
    list_export_fields = ('Project_code', 'ProjectResource_name',)
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-check'
    save_as = False
    save = False
    remove_permissions = ('delete',)
    show_bookmarks = False
    use_related_menu = False
    #
    fields = ['Project_code', 'ProjectResource_name', 'ProjectResource_role',
              'ProjectResource_type', 'ProjectResource_member', 'ProjectResource_serviceitem','ProjectResource_unit',
              'ProjectResource_quantity','ProjectResource_price','ProjectResource_status','ProjectResource_comment',
              'Data_security', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime',]
    readonly_fields = ('Data_owner', 'Data_creator','Data_bu', 'Data_datetime', )
    form_layout = (
        Main(
            Fieldset('基本信息',
                      'Project_code',
                     'ProjectResource_name',
                     'ProjectResource_role', 'ProjectResource_type',
                     ),
            Fieldset('服务内容',
                     'ProjectResource_member', 'Project_days',
                     'ProjectResource_serviceitem', 'ProjectResource_quantity',
                     'ProjectResource_price', 'Project_quantity',
                     css_class='unsort'
                     ),
        ),
        Side(
            Fieldset('审批信息',
                     'ProjectResource_status', 'ProjectResource_comment',
                     ),
            Fieldset('权属信息',
                     'Data_security', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime',
            ),

        ),
    )

    def instance_forms(self):
        super().instance_forms()
        # 判断是否为新建操作
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
    # PSM end for default
    def get_readonly_fields(self):
        if not self.org_obj:  # 新建时
            readonly_fields = []
            return readonly_fields
        else:
            readonly_fields = [
              'Data_security', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime',]  # 修改时
            return readonly_fields
    def formfield_for_dbfield(self, db_field, **kwargs):
       #
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        account_bu = get_account_bu(self)
        if db_field.name == 'ProjectResource_serviceitem':
            kwargs["queryset"] = ItemMaster.objects.filter(Data_bu=account_bu)
        return db_field.formfield(**dict(**kwargs))
    #
# PSM add for Data filter by BU
    def queryset(self):
        qs = super(ProjectResourceAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu=account_bu)
    #
    def save_models(self):
        obj = self.new_obj
        if not obj.ProjectResource_name:
            obj.ProjectResource_name = obj.ProjectResource_code
            obj.save()
        else:
            super(ProjectResourceAdmin, self).save_models()
    # 编辑页面的操作按钮定义
xadmin.site.register(ProjectResourceMaster, ProjectResourceAdmin)
# Project 项目
class ProjectApproveAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    prepopulated_fields = {'slug': ('Project_code',)}
    list_display = ('Project_code', 'Project_name', 'Project_parent', 'Project_status',)
    exclude = ('')
    list_display_links = ('Project_code',)
    search_fields = ('Project_code', 'Project_name')
    list_export_fields = ('Project_code', 'Project_name',)
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-check'
    save_as = False
    save = False
    remove_permissions = ('delete','add')
    show_bookmarks = False
    use_related_menu = False
    #
    fields = ['Project_parent','Project_code', 'Project_name', 'Project_customer',
              'Project_manager', 'Project_method', 'Project_opportunity','Project_days',
              'Project_document','Project_amount','Project_quantity','Project_comment','Project_flowcycle','Project_serviceitem',
              'Project_startdate','Project_enddate', 'Project_nowstage', 'Project_nextstage',
              'Data_security', 'Project_status', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime',]
    readonly_fields = ('Project_status', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime', )
    form_layout = (
        Main(
            Fieldset('基本信息',
                     Row('Project_parent', 'Project_code',),
                     'Project_name',
                     Row('Project_manager', 'Project_method', ),
                     ),
            Fieldset('关联要素',
                     Row('Project_customer','Project_document',),
                     Row('Project_flowcycle', 'Project_opportunity',),
                     css_class='unsort'
                     ),
            Fieldset('服务内容',
                     Row('Project_amount', 'Project_days', ),
                     Row('Project_startdate', 'Project_enddate', ),
                     Row('Project_serviceitem', 'Project_quantity', ),
                     Row('Project_nowstage', 'Project_nextstage', ),
                     css_class='unsort'
                     ),
        ),
        Side(
            Fieldset('审批信息',
                     'Project_status', 'Project_comment',
                     ),
            Fieldset('权属信息',
                     'Data_security', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime',
            ),

        ),
    )

    def instance_forms(self):
        super().instance_forms()
        # 判断是否为新建操作
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
    # PSM end for default
    def get_readonly_fields(self):
        if not self.org_obj:  # 新建时
            readonly_fields = []
            return readonly_fields
        else:
            readonly_fields = ['Project_parent','Project_code', 'Project_name', 'Project_customer',
              'Project_manager', 'Project_method', 'Project_opportunity','Project_days',
              'Project_document','Project_amount','Project_quantity','Project_flowcycle','Project_serviceitem',
              'Project_startdate','Project_enddate', 'Project_nowstage', 'Project_nextstage',
              'Data_security', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime',]  # 修改时
            return readonly_fields
    def formfield_for_dbfield(self, db_field, **kwargs):
       #
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        account_bu = get_account_bu(self)
        if db_field.name == 'Project_serviceitem':
            kwargs["queryset"] = ItemMaster.objects.filter(Data_bu=account_bu)
        if db_field.name == 'Project_flowcycle':
            kwargs["queryset"] = FlowType.objects.filter(Data_bu=account_bu, Flowtype_usage ='P')
        return db_field.formfield(**dict(**kwargs))
    #
# PSM add for Data filter by BU
    def queryset(self):
        qs = super(ProjectApproveAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu=account_bu)
    #
    def save_models(self):
        obj = self.new_obj
        if not obj.Project_name:
            obj.Project_name = obj.Project_code
            obj.save()
        else:
            super(ProjectApproveAdmin, self).save_models()
    # 编辑页面的操作按钮定义
xadmin.site.register(ProjectApprove, ProjectApproveAdmin)
# Contract 合同
class ContractMasterAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    prepopulated_fields = {'slug': ('Contract_code',)}
    list_display = ('Contract_code', 'Contract_name', 'Contract_customer', 'Contract_startdate','Contract_enddate', 'Contract_status',)
    exclude = ('')
    list_display_links = ('Contract_code',)
    search_fields = ('Contract_code', 'Contract_name')
    list_export_fields = ('Contract_code', 'Contract_name',)
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-check'
    save_as = False
    save = False
    remove_permissions = ('delete')
    show_bookmarks = False
    use_related_menu = False
    #
    fields = ['Contract_code', 'Contract_name', 'Contract_customer',
              'Contract_manager', 'Contract_method','Contract_content',
              'Contract_document','Contract_amount', 'Contract_comment',
              'Contract_startdate','Contract_enddate', 'Contract_nowstage', 'Contract_nextstage',
              'Data_security', 'Contract_status', 'Data_owner', 'Data_creator','Data_bu',]
    readonly_fields = ('Contract_status', 'Data_owner', 'Data_creator','Data_bu', )
    form_layout = (
        Main(
            Fieldset('基本信息',
                     Row('Contract_code', 'Contract_name',),
                     Row('Contract_manager', 'Contract_method', ),
                     ),
            Fieldset('关联要素',
                     Row('Contract_customer','Contract_document',),'Contract_content',
                     css_class='unsort'
                     ),
            Fieldset('服务内容',
                     Row('Contract_amount', ),
                     Row('Contract_startdate', 'Contract_enddate', ),
                     Row('Contract_nowstage', 'Contract_nextstage', ),
                     css_class='unsort'
                     ),
        ),
        Side(
            Fieldset('审批信息',
                     'Contract_status', 'Contract_comment',
                     ),
            Fieldset('权属信息',
                     'Data_security', 'Data_owner', 'Data_creator','Data_bu',
            ),

        ),
    )

    def instance_forms(self):
        super().instance_forms()
        # 判断是否为新建操作
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
    # PSM end for default
    def get_readonly_fields(self):
        if not self.org_obj:  # 新建时
            readonly_fields = []
            return readonly_fields
        else:
            readonly_fields = ['Contract_code', 'Contract_name', 'Contract_customer',
              'Contract_manager', 'Contract_method', 'Contract_content',
              'Contract_document', 'Contract_amount',
              'Contract_startdate','Contract_enddate', 'Contract_nowstage', 'Contract_nextstage',
              'Data_security', 'Data_owner', 'Data_creator','Data_bu', ]  # 修改时
            return readonly_fields
    #
# PSM add for Data filter by BU
    def queryset(self):
        qs = super(ContractMasterAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu=account_bu)
    #
    def save_models(self):
        obj = self.new_obj
        if not obj.Contract_name:
            obj.Contract_name = obj.Contract_code
            obj.save()
        else:
            super(ContractMasterAdmin, self).save_models()
    #
xadmin.site.register(ContractMaster, ContractMasterAdmin)




