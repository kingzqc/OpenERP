#
import xadmin
from crm.models import *
from base.models import *
from workflow.models import *
from django.utils.html import format_html
from django.contrib import messages
from random import randint
import datetime
from django.db.models import Q
from xadmin.views.base import get_account_bu  # psm add for get BU
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
# Register your models here.

# 日程目录
class RequestCatalogueAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    prepopulated_fields = {'slug': ('Catalogue_desc',)}
    list_display = ('Catalogue_code', 'Catalogue_desc','Catalogue_type', 'Catalogue_active','Data_bu',)
    exclude = ('')
    list_display_links = ('Catalogue_code',)
    search_fields = ('Catalogue_code', 'Catalogue_desc')
    list_export_fields = ('Catalogue_code', 'Catalogue_desc','Catalogue_type')
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-folder'
    save_as = False
    remove_permissions = ('delete')
    show_bookmarks = False
    use_related_menu = False
    #
    fields = ['Catalogue_code', 'Catalogue_desc','Catalogue_type', 'Catalogue_active','Data_bu','Catalogue_comments', 'Data_security', 'Catalogue_active', 'Data_owner', 'Data_creator','Data_bu', ]
    readonly_fields = ('Catalogue_active', 'Data_owner', 'Data_creator','Data_bu', )
    form_layout = (
        Main(
            Fieldset('基本信息',
                     Row('Catalogue_code', 'Catalogue_desc')
                     ),
            Fieldset('分类信息',
                     'Catalogue_type', 'Catalogue_comments',
                     css_class='unsort'
                     ),
        ),
        Side(
            Fieldset('权属信息',
                     'Data_bu', 'Catalogue_active', 'Data_security', 'Data_owner', 'Data_creator',
            ),
            Fieldset('操 作 栏',
                     Row('actions_column1', ),
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
            #if self.Contact_status =='OK':
            #readonly_fields = self.fields
            #else:
            readonly_fields = ['Data_bu', 'actions_column1']  # 修改时
            return readonly_fields

# PSM add for Data filter by BU
    def queryset(self):
        qs = super(RequestCatalogueAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu=account_bu)

    # 编辑页面的操作按钮定义
    def actions_column1(self, obj):
        #
        parameter_str1 = 'Data_bu={}'.format(str(obj.Data_bu))
        btn_str1 = '<a class="btn btn-primary btn-quick" href="{}" role="button" rel="external nofollow" >' \
                       '进行审核 </a>'
        return format_html(btn_str1, '/base/make_bu_valid/?{}'.format(parameter_str1))

    actions_column1.short_description = ''
xadmin.site.register(RequestCatalogue, RequestCatalogueAdmin)
# 日程类型
class RequestTypeAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    prepopulated_fields = {'slug': ('RequestType_desc',)}
    list_display = ('RequestType_code', 'RequestType_desc', 'RequestType_catalogue', 'RequestType_active', 'Data_bu',)
    exclude = ('')
    list_display_links = ('RequestType_code',)
    search_fields = ('RequestType_code', 'RequestType_desc')
    list_export_fields = ('RequestType_code', 'RequestType_desc', 'RequestType_catalogue')
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-flag-o '
    save_as = False
    # remove_permissions = ('delete', 'add')
    show_bookmarks = False
    use_related_menu = False
    #
    fields = ['RequestType_code', 'RequestType_desc', 'RequestType_catalogue', 'RequestType_active', 'Data_bu',
              'RequestType_comments',
              'Data_security', 'Data_owner', 'Data_creator', 'Data_bu', 'Request_creator',
              'Request_openoverdue', 'Request_approveoverdue', 'Request_realizeoverdue', 'Request_totaloverdue',
              'Request_creatorrole', 'Request_approver', 'Request_approverrole', 'Request_processor',
              'Request_processorrole', 'Request_reopener',
              'Request_reopenerrole', 'Request_realizer', 'Request_realizerrole', 'Request_backer',
              'Request_backerrole', 'Request_deleter', 'Request_deleterrole',
              'Request_mustcont', 'Request_mustcust', 'Request_mustoppo', 'Request_mustproj', 'Request_mustitem']
    readonly_fields = ('RequestType_active', 'Data_owner', 'Data_creator', 'Data_datetime',)
    form_layout = (
        Main(
            Fieldset('基本信息',
                     Row('RequestType_code', 'RequestType_desc')
                     ),
            Fieldset('流程设置（使用时人优先于角色）',
                     Row('Request_creator', 'Request_creatorrole'),
                     Row('Request_approver', 'Request_approverrole'),
                     Row('Request_realizer', 'Request_realizerrole'),
                     Row('Request_processor', 'Request_processorrole'),
                     Row('Request_reopener', 'Request_reopenerrole'),
                     Row('Request_backer', 'Request_backerrole'),
                     Row('Request_deleter', 'Request_deleterrole'),
                     ),
            Fieldset('过期时长设置',
                     Row('Request_openoverdue', 'Request_approveoverdue'),
                     Row('Request_realizeoverdue', 'Request_totaloverdue'),
                     ),
            Fieldset('分类信息',
                     'RequestType_catalogue',
                     'RequestType_active',
                     'RequestType_comments', css_class='unsort'
                     ),
        ),
        Side(
            Fieldset('必填项设置',
                     'Request_mustcont', 'Request_mustcust', 'Request_mustoppo', 'Request_mustproj', 'Request_mustitem',
                     ),
            Fieldset('权属信息',
                     'Data_bu', 'Data_security', 'Data_owner', 'Data_creator',
                     ),
        ),
    )

    def instance_forms(self):
        super().instance_forms()
        # 判断是否为新建操作
        if not self.org_obj:
            # PSM add for BU check
            if not self.user.is_superuser:
                account_bu = get_account_bu(self)  # 获取账号所属BU
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
            readonly_fields = ['Data_bu', ]  # 修改时
            return readonly_fields

    # PSM add for Data filter by BU
    def queryset(self):
        qs = super(RequestTypeAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            account_bu = get_account_bu(self)  # 获取账号所属BU
            return qs.filter(Data_bu=account_bu)
xadmin.site.register(RequestType, RequestTypeAdmin)
#
class FlowRequestTypeInlineFormset(forms.models.BaseInlineFormSet):
    remove_permissions = ('delete',)
    # 页面字段内容的校验
    def clean(self):
        flowtype = None
        requesttype = None
        if any(self.errors):
            return
        flowtype = self.instance   # 取得的是项目code
        #print(flowtype)
        for f in self.forms:  # forms是inline的表格， f代表每一行内容
            stagedesc = f.cleaned_data.get('Flowcycle_stagedesc')
            stage = f.cleaned_data.get('Flowcycle_stage')
            databu = f.cleaned_data.get('Data_bu')
            if stagedesc == None and stage != None:
                raise forms.ValidationError(u'阶段说明必须填入内容,请更正！', code='invalid')
            if stage == None and stagedesc != None:
                raise forms.ValidationError(('阶段中没有内容，请填写！'), code='invalid')
            if databu !=None and stage == None and stagedesc == None:
                raise forms.ValidationError(('没有内容，请填写！'), code='invalid')
            if databu ==None and (stage != None or stagedesc != None):
                raise forms.ValidationError(('BU没有内容，请填写！'), code='invalid')
            requesttype = f.save(commit=False)
        #if flowtype != None:
         #   print(flowtype.Flowtype_active)
         #   if flowtype.Flowtype_active == True:
          #      raise forms.ValidationError((str(flowtype) + u'状态不合适，不能修改内容，请直接退出！'), code='invalid')
class FlowRequestTypeInline(object):
    model = FlowCycleMaster
    formset = FlowRequestTypeInlineFormset
    extra = 1
    style = 'table'
    fields = ['Flowcycle_stagedesc', 'Flowcycle_stage',
              'Data_security', 'Data_owner', 'Data_creator', 'Data_bu', 'Data_datetime',]
    exclude = ['Data_security', 'Data_owner', 'Data_creator', 'Data_datetime',]
    readonly_fields = ()
    remove_permissions = ('delete',)
    #def get_extra(self):
    #    if not self.org_obj:
    #        extra = 0
    #    else:
    #        extra = 0
    #    return extra
    def ResetAuth(self):
        # 重新定义此函数，限制普通用户的增删改权限
        if self.org_obj.Flowtype_active == False:
            self.remove_permissions = ()
        else:
            self.remove_permissions = ('delete', 'add',)
        return self.remove_permissions
    def instance_forms(self):
        super().instance_forms()
        # 判断是否为新建操作
        if not self.org_obj:
            # PSM add for BU check
            if not self.user.is_superuser:
                account_bu = get_account_bu(self)  # 获取账号所属BU
            else:
                account_bu = '*ALL'
            self.form_obj.initial['Data_bu_id'] = account_bu
            self.form_obj.initial['Data_bu'] = account_bu
            self.form_obj.initial['Data_owner'] = self.request.user.id
            self.form_obj.initial['Data_creator'] = self.request.user.id
        else:
            pass
    def get_readonly_fields(self):
        if not self.org_obj:  # 新建时
            readonly_fields = []
            return readonly_fields
        else:
            if self.org_obj.Flowtype_active == True:
                readonly_fields = ['Flowcycle_stagedesc', 'Flowcycle_stage','Data_bu']  # 启用时
            else:
                readonly_fields = []  # 没启用
            return readonly_fields
# 销售周期
class FlowTypeAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    prepopulated_fields = {'slug': ('Flowtype_desc',)}
    list_display = ('Flowtype_code', 'Flowtype_desc', 'Flowtype_usage', 'Data_bu',)
    exclude = ('')
    list_display_links = ('Flowtype_code',)
    search_fields = ('Flowtype_code', 'Flowtype_desc')
    list_export_fields = ('Flowtype_code', 'Flowtype_desc')
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-flag-o '
    save_as = False
    remove_permissions = ('delete',)
    show_bookmarks = False
    use_related_menu = False
    #
    fields = ['Flowtype_code', 'Flowtype_desc', 'Flowtype_usage',
              'Data_security', 'Data_owner', 'Data_creator', 'Data_bu', 'Flowtype_active']
    readonly_fields = ('Data_owner', 'Data_creator', 'Data_datetime',)
    form_layout = (
        Main(
            Fieldset('基本信息',
                     'Flowtype_code', 'Flowtype_desc', 'Flowtype_usage',
                     ),
        ),
        Side(
            Fieldset('权属信息',
                     'Data_bu', 'Data_security', 'Data_owner', 'Data_creator', 'Flowtype_active',
                     ),
        ),
    )
    inlines = [FlowRequestTypeInline]

    def instance_forms(self):
        super().instance_forms()
        # 判断是否为新建操作
        if not self.org_obj:
            # PSM add for BU check
            if not self.user.is_superuser:
                account_bu = get_account_bu(self)  # 获取账号所属BU
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
            readonly_fields = ['Data_bu']  # 修改时
            return readonly_fields
# PSM add for Data filter by BU
    def queryset(self):
        qs = super(FlowTypeAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            account_bu = get_account_bu(self) # 获取账号所属BU
            return qs.filter(Data_bu=account_bu)
    #
    def save_models(self):
        obj = self.new_obj
        if not obj.Flowtype_code:
            obj.Flowtype_desc = obj.Flowtype_code
            obj.save()
        else:
            super(FlowTypeAdmin, self).save_models()

xadmin.site.register(FlowType, FlowTypeAdmin)

# 工作流
class RequestMasterAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    prepopulated_fields = {'slug': ('Request_desc',)}
    list_display = ('Dummy_id', 'Request_type', 'Request_desc','Request_customer', 'Request_opportunity', 'Request_project', 'Request_usage', 'Request_cancel', 'Request_status','actions_column',)
    exclude = ['actions_column']
    list_display_links = ('Dummy_id',)
    search_fields = ('Request_desc','Dummy_id',)
    list_filter = ['Request_opportunity','Request_project','Request_customer','Request_status',]
    ordering =['Dummy_id',]
    list_export_fields = ('Request_type', 'Request_desc',)
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-font'
    save_as = False
    #remove_permissions = ('delete',)
    show_bookmarks = False
    use_related_menu = False
    #
    fields = ['Dummy_id', 'Request_type','Request_desc', 'Request_account','Request_comments','Request_mainresource','Request_auxresource','Request_basecompetence',
              'Request_duration', 'Request_initdate','Request_inittime',  'Request_enddate', 'Request_endtime','Request_request', 'Request_nextrequest',
              'Request_customer','Request_contact','Request_opportunity','Request_project','Request_serviceitem',
              'Request_quantity','Request_price', 'Request_amount','Request_flowcycle', 'Request_usage','Request_cancel','Request_isyes',
              'Data_security', 'Request_status', 'Data_owner', 'Data_creator', 'Data_approver', 'Data_realizer', 'Data_processor','Data_bu',]
    readonly_fields = ('Request_status', 'Data_owner', 'Data_creator','Data_bu', 'Data_datetime','Request_flowcycle', )
    form_layout = (
        Main(
            Fieldset('基本信息',
                     Row('Dummy_id','Request_usage',),
                     Row('Request_flowcycle','Request_type',),
                     Row('Request_desc','Request_account',),
                     ),
            Fieldset('相关要素',
                     Row('Request_customer','Request_contact',),
                     Row('Request_opportunity','Request_project',),
                     Row('Request_mainresource', 'Request_auxresource',),
                     Row('Request_request', 'Request_nextrequest',),
                     css_class='unsort'
                     ),
            Fieldset('计划服务内容',
                     Row('Request_initdate', 'Request_inittime',),
                     Row('Request_enddate', 'Request_endtime', ),
                     Row('Request_serviceitem', ),
                     Row('Request_duration','Request_quantity', ),
                     Row('Request_price', 'Request_amount', ),
                     css_class='unsort'
                     ),
        ),
        Side(
            Fieldset('审批信息',
                     'Request_comments',
                     'Request_status',
                     'Request_isyes',
                     'Request_cancel',
                     ),
            Fieldset('权属信息',
                     'Data_bu','Data_security', 'Data_owner', 'Data_creator', 'Data_approver', 'Data_realizer', 'Data_processor',
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
            self.form_obj.initial['Dummy_id'] = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + str(
                randint(100, 199))
        else:
            pass
    # PSM end for default
    def get_readonly_fields(self):
        if not self.org_obj:  # 新建时
            readonly_fields = []
        else:
            readonly_fields = ['Data_bu','Request_flowcycle','Request_type','Dummy_id','Request_usage',]  # 修改时
        return readonly_fields

# PSM add for Data filter by BU
    def queryset(self):
        qs = super(RequestMasterAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs.filter(Request_status__gt ='')
        else:
            account_bu = get_account_bu(self)
            #print(account_bu,self.request.user.id)
            return qs.filter((Q(Data_owner_id__exact=self.request.user.id) | Q(Data_approver_id__exact=self.request.user.id) | Q(Data_realizer_id__exact=self.request.user.id) | Q(Data_processor_id__exact=self.request.user.id)), Data_bu_id=account_bu,Request_status__gt ='')
    #
    # 列表页面的操作按钮 定义
    def actions_column(self,obj):
        #
        if obj.Dummy_id:
            if obj.Request_cancel == True: # 判断是否 “暂停”= True
                admin_url = self.get_admin_url(
                    '%s_%s_change' % ('workflow', 'requestreopen'),
                    obj.Data_id)
                btn = '<a class="btn btn-info btn-xs" href="{}" role="button" rel="external nofollow">重开</a>'
                return format_html(btn, admin_url)
            elif obj.Request_status == '00': # 日程状态为 “待办”
                if obj.Data_approver_id == self.request.user.id:
                    admin_url00 = self.get_admin_url(
                        '%s_%s_change' % ('workflow', 'requestapprove'),
                        obj.Data_id)
                    btn00 = '<a class="btn btn-info btn-xs" href="{}" role="button" rel="external nofollow">批准</a>'
                    return format_html(btn00, admin_url00)
                else:
                    if obj.Data_delegator_id == self.request.user.id:
                        admin_url00 = self.get_admin_url(
                            '%s_%s_change' % ('workflow', 'requestapprove'),
                            obj.Data_id)
                        btn00 = '<a class="btn btn-info btn-xs" href="{}" role="button" rel="external nofollow">委托批准</a>'
                        return format_html(btn00, admin_url00)
                    else:
                        admin_url = ''
                        btn = '<a class="btn btn-info btn-xs" href="{}" role="button" rel="external nofollow">无</a>'
                        return format_html(btn, admin_url)
            elif obj.Request_status == '10': # 日程状态为 “已批准”
                if obj.Data_approver_id != obj.Data_realizer_id:
                    if obj.Data_approver_id == self.request.user.id:
                        admin_url = self.get_admin_url(
                            '%s_%s_change' % ('workflow', 'requestbackward'),
                            obj.Data_id)
                        btn = '<a class="btn btn-info btn-xs" href="{}" role="button" rel="external nofollow">回退</a>'
                        return format_html(btn, admin_url)
                    else:
                        if obj.Data_realizer_id == self.request.user.id:
                            admin_url10 = self.get_admin_url(
                                '%s_%s_change' % ('workflow', 'requestrealize'),
                                obj.Data_id)
                            btn10 = '<a class="btn btn-info btn-xs" href="{}" role="button" rel="external nofollow">实现</a>'
                            return format_html(btn10, admin_url10)
                        else:
                            admin_url = ''
                            btn = '<a class="btn btn-info btn-xs" href="{}" role="button" rel="external nofollow">无</a>'
                            return format_html(btn, admin_url)
                else:
                    if obj.Data_approver_id == self.request.user.id and obj.Data_realizer_id == self.request.user.id:
                        admin_url = self.get_admin_url(
                            '%s_%s_change' % ('workflow', 'requestbackward'),
                            obj.Data_id)
                        btn = '<a class="btn btn-info btn-xs" href="{}" role="button" rel="external nofollow">回退</a>'
                        #
                        admin_url10 = self.get_admin_url(
                            '%s_%s_change' % ('workflow', 'requestrealize'),
                            obj.Data_id)
                        btn10 = '<a class="btn btn-info btn-xs" href="{}" role="button" rel="external nofollow">实现</a>'
                        return format_html(btn10, admin_url10) + format_html(btn, admin_url)
                    else:
                        admin_url = ''
                        btn = '<a class="btn btn-info btn-xs" href="{}" role="button" rel="external nofollow">无</a>'
                        return format_html(btn, admin_url)
            elif obj.Request_status == '20': # 日程状态为 “已实现”
                if obj.Data_processor_id == self.request.user.id:
                    admin_url20 = self.get_admin_url(
                        '%s_%s_change' % ('workflow', 'requestprocess'),
                        obj.Data_id)
                    btn20 = '<a class="btn btn-info btn-xs" href="{}" role="button" rel="external nofollow">处理</a>'
                    return format_html(btn20, admin_url20)
                else:
                    admin_url = ''
                    btn = '<a class="btn btn-info btn-xs" href="{}" role="button" rel="external nofollow">无</a>'
                    return format_html(btn, admin_url)
            elif obj.Request_status == '30':  # 日程状态为 “已处理”
                if obj.Data_processor_id == self.request.user.id:
                    admin_url30 = self.get_admin_url(
                        '%s_%s_change' % ('workflow', 'requestbackward'),
                        obj.Data_id)
                    btn30 = '<a class="btn btn-info btn-xs" href="{}" role="button" rel="external nofollow">回退</a>'
                    return format_html(btn30, admin_url30)
                else:
                    admin_url = ''
                    btn = '<a class="btn btn-info btn-xs" href="{}" role="button" rel="external nofollow">无</a>'
                    return format_html(btn, admin_url)
            else:
                admin_url = ''
                btn = '<a class="btn btn-info btn-xs" href="{}" role="button" rel="external nofollow">无</a>'
                return format_html(btn, admin_url)
        else:
            admin_url = ''
            btn = '<a class="btn btn-info btn-xs" href="{}" role="button" rel="external nofollow">无</a>'
            return format_html(btn, admin_url)
    actions_column.short_description = '操 作 项'
xadmin.site.register(RequestMaster, RequestMasterAdmin)
# Project 工作流approve
class RequestApproveAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    prepopulated_fields = {'slug': ('Request_desc',)}
    list_display = (
    'Dummy_id', 'Request_type', 'Request_desc', 'Request_customer', 'Request_opportunity', 'Request_project',
    'Request_usage', 'Data_bu', 'Request_status',)
    exclude = ('')
    list_display_links = ('Dummy_id',)
    search_fields = ('Request_desc', 'Dummy_id',)
    list_filter = ['Request_opportunity', 'Request_project', 'Request_customer']
    ordering = ['-Dummy_id', ]
    list_export_fields = ('Request_type', 'Request_desc',)
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa fa-check'
    save_as = False
    remove_permissions = ('delete', 'add',)
    show_bookmarks = False
    use_related_menu = False
    hidden_menu = True
    #
    fields = ['Dummy_id', 'Request_type', 'Request_desc', 'Request_account', 'Request_comments','Request_mainresource','Request_auxresource',
              'Request_duration', 'Request_initdate','Request_inittime', 'Request_enddate', 'Request_endtime','Request_request', 'Request_nextrequest',
              'Request_customer', 'Request_contact', 'Request_opportunity', 'Request_project', 'Request_serviceitem',
              'Request_quantity', 'Request_price', 'Request_amount', 'Request_flowcycle', 'Request_usage',
              'Request_isyes', 'Data_delegator',]
    readonly_fields = ('Dummy_id','Request_type', 'Request_desc', 'Request_account',
                       'Request_flowcycle','Request_usage','Request_request', 'Request_nextrequest',
                       'Request_customer', 'Request_contact', 'Request_opportunity', 'Request_project',
                       'Request_serviceitem',)
    form_layout = (
        Main(
            Fieldset('基本信息',
                     Row('Dummy_id', 'Request_usage', ),
                     Row('Request_flowcycle', 'Request_type', ),
                     Row('Request_desc', 'Request_account', ),
                     ),
            Fieldset('相关要素',
                     Row('Request_customer', 'Request_contact', ),
                     Row('Request_opportunity', 'Request_project', ),
                     Row('Request_mainresource', 'Request_auxresource',),
                     Row('Request_request', 'Request_nextrequest', ),
                     css_class='unsort'
                     ),
            Fieldset('计划服务内容',
                     Row('Request_initdate', 'Request_inittime', ),
                     Row('Request_enddate', 'Request_endtime', ),
                     Row('Request_serviceitem', ),
                     Row('Request_duration', 'Request_quantity', ),
                     Row('Request_price', 'Request_amount', ),
                     css_class='unsort'
                     ),
        ),
        Side(
            Fieldset('操作参考信息',
                     'Request_comments', 'Request_isyes', 'Data_delegator',
                     ),
        )
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
    def formfield_for_dbfield(self, db_field, **kwargs):
       #
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        #
        account_bu = get_account_bu(self)  # 获取账号所属BU
        if db_field.name == 'Data_delegator':
            kwargs["queryset"] = UserProfile.objects.filter(Data_bu=account_bu)
        return db_field.formfield(**dict(**kwargs))
# PSM add for Data filter by BU
    def queryset(self):
        qs = super(RequestApproveAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs.filter(Request_status__exact ='00',Request_cancel__exact= False)
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu_id=account_bu, Request_status__exact ='00', Request_cancel__exact= False, Data_approver_id__exact=self.request.user.id)
    #
    def save_models(self):
        obj = self.new_obj
        #
        approve = obj.Request_isyes
        obj.Data_datetime = datetime.datetime.now()
        if approve is True:
            if obj.Data_delegator_id:
                obj.Request_comments += '已委托！' + 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
                obj.Request_isyes= False
                #
                obj.save()
            else:
                obj.Request_comments += '同意！' + 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
                obj.Request_status = '10'
                obj.Request_isyes = False
                # 批准后把计划的内容填入实际中，做为实际的默认值
                obj.Request_actinitdate = obj.Request_initdate
                obj.Request_actenddate = obj.Request_enddate
                obj.Request_actinittime = obj.Request_inittime
                obj.Request_actendtime = obj.Request_endtime
                obj.Request_actduration = obj.Request_duration
                obj.Request_actquantiyt = obj.Request_quantity
                obj.Request_actprice = obj.Request_price
                obj.Request_actamount = obj.Request_amount
                #
                obj.save()
        else:
            if not obj.Data_delegator_id:
                obj.Request_comments += '不同意！' + 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
                obj.Request_isyes = False
                obj.Data_delegator = None
                obj.save()
            else:
                obj.Request_comments += 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
                obj.Data_delegator = None
                super(RequestApproveAdmin, self).save_models()
xadmin.site.register(RequestApprove, RequestApproveAdmin)

# Project 工作流 realize
class RequestRealizeAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    prepopulated_fields = {'slug': ('Request_desc',)}
    list_display = (
        'Dummy_id', 'Request_type', 'Request_desc', 'Request_customer', 'Request_opportunity', 'Request_project',
        'Request_usage', 'Request_status',)
    exclude = ('')
    list_display_links = ('Dummy_id',)
    search_fields = ('Request_desc', 'Dummy_id',)
    list_filter = ['Request_opportunity', 'Request_project', 'Request_customer']
    list_export_fields = ('Request_type', 'Request_desc',)
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-keyboard-o'
    save_as = False
    save = False
    remove_permissions = ('delete', 'add')
    show_bookmarks = False
    use_related_menu = False
    hidden_menu = True
    #
    fields = ['Dummy_id', 'Request_type', 'Request_desc', 'Request_account', 'Request_comments','Request_mainresource','Request_auxresource',
              'Request_duration', 'Request_initdate','Request_inittime', 'Request_enddate','Request_endtime',  'Request_request', 'Request_nextrequest',
              'Request_customer', 'Request_contact', 'Request_opportunity', 'Request_project', 'Request_serviceitem',
              'Request_quantity', 'Request_price', 'Request_amount', 'Request_flowcycle', 'Request_usage',
              'Request_isyes', 'Request_actinitdate', 'Request_actenddate','Request_actduration', 'Request_actquantity',
                'Request_actprice', 'Request_actamount',]
    readonly_fields = ('Dummy_id', 'Request_type', 'Request_desc', 'Request_account',
                       'Request_flowcycle', 'Request_usage', 'Request_request', 'Request_nextrequest',
                       'Request_customer', 'Request_contact', 'Request_opportunity', 'Request_project',
                       'Request_initdate', 'Request_enddate', 'Request_inittime', 'Request_endtime',
                       'Request_duration', 'Request_quantity',
                       'Request_price', 'Request_amount',
                       'Request_serviceitem',)
    form_layout = (
        Main(
            Fieldset('实际服务内容',
                     Row('Request_actinitdate', 'Request_actinittime', ),
                     Row('Request_actenddate', 'Request_actendtime', ),
                     Row('Request_actduration', 'Request_actquantity', ),
                     Row('Request_actprice', 'Request_actamount', ),
                     css_class='unsort'
                     ),
            Fieldset('基本信息',
                     Row('Dummy_id', 'Request_usage', ),
                     Row('Request_flowcycle', 'Request_type', ),
                     Row('Request_desc', 'Request_account', ),
                     ),
            Fieldset('相关要素',
                     Row('Request_customer', 'Request_contact', ),
                     Row('Request_opportunity', 'Request_project', ),
                     Row('Request_mainresource', 'Request_auxresource',),
                     Row('Request_request', 'Request_nextrequest', ),
                     css_class='unsort'
                     ),
            Fieldset('计划服务内容',
                     Row('Request_initdate', 'Request_inittime', ),
                     Row('Request_enddate', 'Request_endtime', ),
                     Row('Request_serviceitem', ),
                     Row('Request_duration', 'Request_quantity', ),
                     Row('Request_price', 'Request_amount', ),
                     css_class='unsort'
                     ),
        ),
        Side(
            Fieldset('操作参考信息',
                     'Request_comments', 'Request_isyes',
                     ),
        )
    )
# PSM add for Data filter by BU
    def queryset(self):
        qs = super(RequestRealizeAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs.filter(Request_status__exact='10',Request_cancel__exact=False)
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu_id=account_bu, Request_status__exact='10', Request_cancel__exact=False, Data_realizer_id__exact=self.request.user.id)
    #
    def save_models(self):
        obj = self.new_obj
        #
        realize = obj.Request_isyes
        obj.Data_datetime = datetime.datetime.now()
        if realize is True:
            obj.Request_comments += '已实现！' + 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
            obj.Request_status = '20'
            obj.Request_isyes= False
            obj.save()
            # 工作流在实现后，如果存在后续request, 启动它
            if obj.Request_nextrequest:
                rm = RequestMaster.objects.filter(Data_bu=obj.Data_bu, Dummy_id=obj.Request_nextrequest).first()
                if rm:
                    if rm.Request_status not in ['00','10','20','30']:
                        rm.Request_status ='00'
                        rm.Data_datetime = datetime.datetime.now()
                        rm.save()
                #   工作流在实现后， 更新商机中的当前状态 request
                om = OpportunityMaster.objects.filter(Data_bu=obj.Data_bu, Data_id=obj.Request_opportunity_id).first()
                if om:
                    om.Opportunity_nowstage = obj.Request_nextrequest
                    om.Opportunity_currentamount = obj.Request_actamount
                    om.save()
            #
            messages.info(self.request, str(obj.Dummy_id + '实现操作已经完成'))
        if realize is False:
            obj.Request_comments += '没实现！' + 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
            obj.Request_isyes = False
            obj.save()
            messages.info(self.request, str(obj.Dummy_id + '没有进行实现操作'))
        else:
            obj.Request_comments += 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
            super(RequestRealizeAdmin, self).save_models()

xadmin.site.register(RequestRealize, RequestRealizeAdmin)
# 工作流process
class RequestProcessAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    prepopulated_fields = {'slug': ('Request_desc',)}
    list_display = (
        'Dummy_id', 'Request_type', 'Request_desc', 'Request_customer', 'Request_opportunity', 'Request_project',
        'Request_usage', 'Request_status',)
    exclude = ('')
    list_display_links = ('Dummy_id',)
    search_fields = ('Request_desc', 'Dummy_id',)
    list_filter = ['Request_opportunity', 'Request_project', 'Request_customer']
    list_export_fields = ('Request_type', 'Request_desc',)
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-save'
    save_as = False
    save = False
    remove_permissions = ('delete', 'add')
    show_bookmarks = False
    use_related_menu = False
    hidden_menu = True
    #
    fields = ['Dummy_id', 'Request_type', 'Request_desc', 'Request_account', 'Request_comments','Request_mainresource','Request_auxresource',
              'Request_duration', 'Request_initdate', 'Request_enddate', 'Request_inittime', 'Request_endtime', 'Request_request', 'Request_nextrequest',
              'Request_customer', 'Request_contact', 'Request_opportunity', 'Request_project', 'Request_serviceitem',
              'Request_quantity', 'Request_price', 'Request_amount', 'Request_flowcycle', 'Request_usage',
              'Request_isyes','Request_actinitdate', 'Request_actenddate','Request_actinittime', 'Request_actendtime','Request_actduration', 'Request_actquantity',
                'Request_actprice', 'Request_actamount',]
    readonly_fields = ('Dummy_id', 'Request_type', 'Request_desc', 'Request_account',
                       'Request_flowcycle', 'Request_usage', 'Request_request', 'Request_nextrequest',
                       'Request_customer', 'Request_contact', 'Request_opportunity', 'Request_project',
                       'Request_serviceitem', 'Request_initdate', 'Request_enddate', 'Request_inittime', 'Request_endtime', 'Request_duration',
                       'Request_quantity', 'Request_price', 'Request_amount',
                       'Request_actinitdate', 'Request_actenddate', 'Request_actinittime', 'Request_actendtime','Request_actduration', 'Request_actquantity',
                       'Request_actprice', 'Request_actamount',)
    form_layout = (
        Main(
            Fieldset('基本信息',
                     Row('Dummy_id', 'Request_usage', ),
                     Row('Request_flowcycle', 'Request_type', ),
                     Row('Request_desc', 'Request_account', ),
                     ),
            Fieldset('相关要素',
                     Row('Request_customer', 'Request_contact', ),
                     Row('Request_opportunity', 'Request_project', ),
                     Row('Request_mainresource', 'Request_auxresource',),
                     Row('Request_request', 'Request_nextrequest', ),
                     css_class='unsort'
                     ),
            Fieldset('计划服务内容',
                     Row('Request_initdate', 'Request_inittime', ),
                     Row('Request_enddate', 'Request_endtime', ),
                     Row('Request_serviceitem', ),
                     Row('Request_duration', 'Request_quantity', ),
                     Row('Request_price', 'Request_amount', ),
                     css_class='unsort'
                     ),
            Fieldset('实际服务内容',
                     Row('Request_actinitdate', 'Request_actinittime', ),
                     Row('Request_actenddate', 'Request_actendtime', ),
                     Row('Request_actduration', 'Request_actquantity', ),
                     Row('Request_actprice', 'Request_actamount', ),
                     css_class='unsort'
                     ),
        ),
        Side(
            Fieldset('操作参考信息',
                     'Request_comments', 'Request_isyes',
                     ),
        )
    )

# PSM add for Data filter by BU
    def queryset(self):
        qs = super(RequestProcessAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs.filter(Request_status__exact ='20', Request_cancel__exact= False)
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu_id=account_bu, Request_status__exact ='20',Request_cancel__exact= False, Data_processor_id__exact=self.request.user.id)
    #
    def save_models(self):
        obj = self.new_obj
        #
        process = obj.Request_isyes
        obj.Data_datetime = datetime.datetime.now()
        if process is True:
            obj.Request_comments += '已处理！' + 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
            obj.Request_status = '30'
            obj.Request_isyes = False
            obj.save()
            messages.info(self.request, str(obj.Dummy_id + '处理操作已经完成'))
        if process is False:
            obj.Request_comments += '没处理！' + 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
            obj.Request_isyes = False
            obj.save()
            messages.info(self.request, str(obj.Dummy_id + '没有进行处理操作'))
        else:
            obj.Request_comments += 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
            super(RequestProcessAdmin, self).save_models()
xadmin.site.register(RequestProcess, RequestProcessAdmin)
# 工作流 Reopen
class RequestReopenAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    prepopulated_fields = {'slug': ('Request_desc',)}
    list_display = ('Dummy_id', 'Request_type', 'Request_desc', 'Request_customer', 'Request_opportunity', 'Request_project',
        'Request_usage', 'Request_cancel', 'Request_status',)
    exclude = ('')
    list_display_links = ('Dummy_id',)
    search_fields = ('Request_desc', 'Dummy_id',)
    list_filter = ['Request_opportunity', 'Request_project', 'Request_customer']
    list_export_fields = ('Request_type', 'Request_desc',)
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-save'
    save_as = False
    save = False
    remove_permissions = ('delete', 'add')
    show_bookmarks = False
    use_related_menu = False
    hidden_menu = True
    #
    fields = ['Dummy_id', 'Request_type', 'Request_desc', 'Request_account', 'Request_comments','Request_mainresource','Request_auxresource',
              'Request_duration', 'Request_initdate', 'Request_enddate','Request_inittime', 'Request_endtime', 'Request_request', 'Request_nextrequest',
              'Request_customer', 'Request_contact', 'Request_opportunity', 'Request_project', 'Request_serviceitem',
              'Request_quantity', 'Request_price', 'Request_amount', 'Request_flowcycle', 'Request_usage',
              'Request_isyes', 'Request_actinitdate', 'Request_actenddate', 'Request_actinittime', 'Request_actendtime', 'Request_actduration',
              'Request_actquantity',
              'Request_actprice', 'Request_actamount', ]
    readonly_fields = ('Dummy_id', 'Request_type', 'Request_desc', 'Request_account',
                       'Request_flowcycle', 'Request_usage', 'Request_request', 'Request_nextrequest',
                       'Request_customer', 'Request_contact', 'Request_opportunity', 'Request_project',
                       'Request_serviceitem','Request_initdate', 'Request_enddate','Request_inittime', 'Request_endtime','Request_duration',
                       'Request_quantity', 'Request_price', 'Request_amount',
                       'Request_actinitdate', 'Request_actenddate','Request_actinittime', 'Request_actendtime', 'Request_actduration', 'Request_actquantity',
                       'Request_actprice', 'Request_actamount',)
    form_layout = (
        Main(
            Fieldset('基本信息',
                     Row('Dummy_id', 'Request_usage', ),
                     Row('Request_flowcycle', 'Request_type', ),
                     Row('Request_desc', 'Request_account', ),
                     ),
            Fieldset('相关要素',
                     Row('Request_customer', 'Request_contact', ),
                     Row('Request_opportunity', 'Request_project', ),
                     Row('Request_mainresource', 'Request_auxresource',),
                     Row('Request_request', 'Request_nextrequest', ),
                     css_class='unsort'
                     ),
            Fieldset('计划服务内容',
                     Row('Request_initdate', 'Request_inittime', ),
                     Row('Request_enddate', 'Request_endtime', ),
                     Row('Request_serviceitem', ),
                     Row('Request_duration', 'Request_quantity', ),
                     Row('Request_price', 'Request_amount', ),
                     css_class='unsort'
                     ),
            Fieldset('实际服务内容',
                     Row('Request_actinitdate', 'Request_actinittime', ),
                     Row('Request_actenddate', 'Request_actendtime', ),
                     Row('Request_actduration', 'Request_actquantity', ),
                     Row('Request_actprice', 'Request_actamount', ),
                     css_class='unsort'
                     ),
        ),
        Side(
            Fieldset('操作参考信息',
                     'Request_comments', 'Request_isyes',
                     ),
        )
    )

    # PSM add for Data filter by BU
    def queryset(self):
        qs = super(RequestReopenAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs.filter(Request_cancel__exact= True, Request_status__gt ='')
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu_id=account_bu, Request_cancel__exact= True, Request_status__gt ='', Data_reopener_id__exact=self.request.user.id)
    #
    def save_models(self):
        obj = self.new_obj
        #
        reopen = obj.Request_isyes
        obj.Data_datetime = datetime.datetime.now()
        if reopen is True:
            obj.Request_comments += '已重开！' + 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
            obj.Request_cancel = False
            obj.Request_isyes = False
            obj.save()
            messages.info(self.request, str(obj.Dummy_id + '重开操作已经完成'))
        if reopen is False:
            obj.Request_comments += '没重开！' + 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
            obj.Request_cancel = True
            obj.Request_isyes = True
            obj.save()
            messages.info(self.request, str(obj.Dummy_id + '没有进行重开操作'))
        else:
            obj.Request_comments += 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
            super(RequestReopenAdmin, self).save_models()

xadmin.site.register(RequestReopen, RequestReopenAdmin)
# 工作流 backward
class RequestBackwardAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    prepopulated_fields = {'slug': ('Request_desc',)}
    list_display = (
        'Dummy_id', 'Request_type', 'Request_desc', 'Request_customer', 'Request_opportunity', 'Request_project',
        'Request_usage', 'Request_cancel', 'Request_status',)
    exclude = ('')
    list_display_links = ('Dummy_id',)
    search_fields = ('Request_desc', 'Dummy_id',)
    list_filter = ['Request_opportunity', 'Request_project', 'Request_customer']
    list_export_fields = ('Request_type', 'Request_desc',)
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-save'
    save_as = False
    save = False
    remove_permissions = ('delete', 'add')
    show_bookmarks = False
    use_related_menu = False
    hidden_menu = True
    #
    fields = ['Dummy_id', 'Request_type', 'Request_desc', 'Request_account', 'Request_comments','Request_mainresource','Request_auxresource','Request_basecompetence',
              'Request_duration', 'Request_initdate', 'Request_enddate', 'Request_inittime', 'Request_endtime','Request_request', 'Request_nextrequest',
              'Request_customer', 'Request_contact', 'Request_opportunity', 'Request_project', 'Request_serviceitem',
              'Request_quantity', 'Request_price', 'Request_amount', 'Request_flowcycle', 'Request_usage',
              'Request_isyes', 'Request_actinitdate', 'Request_actenddate', 'Request_actinittime', 'Request_actendtime', 'Request_actduration',
              'Request_actquantity','Request_status',
              'Request_actprice', 'Request_actamount', ]
    readonly_fields = ('Dummy_id', 'Request_type', 'Request_desc', 'Request_account',
                       'Request_flowcycle', 'Request_usage', 'Request_request', 'Request_nextrequest',
                       'Request_customer', 'Request_contact', 'Request_opportunity', 'Request_project',
                       'Request_serviceitem', 'Request_initdate', 'Request_enddate',  'Request_inittime', 'Request_endtime', 'Request_duration',
                       'Request_quantity', 'Request_price', 'Request_amount',
                       'Request_actinitdate', 'Request_actenddate','Request_actinittime', 'Request_actendtime', 'Request_actduration', 'Request_actquantity',
                       'Request_actprice', 'Request_actamount',)
    form_layout = (
        Main(
            Fieldset('基本信息',
                     Row('Dummy_id', 'Request_usage', ),
                     Row('Request_flowcycle', 'Request_type', ),
                     Row('Request_desc', 'Request_account', ),
                     ),
            Fieldset('相关要素',
                     Row('Request_customer', 'Request_contact', ),
                     Row('Request_opportunity', 'Request_project', ),
                     Row('Request_mainresource', 'Request_auxresource',),
                     Row('Request_request', 'Request_nextrequest', ),
                     css_class='unsort'
                     ),
            Fieldset('计划服务内容',
                     Row('Request_initdate', 'Request_inittime', ),
                     Row('Request_enddate', 'Request_endtime', ),
                     Row('Request_serviceitem', ),
                     Row('Request_duration', 'Request_quantity', ),
                     Row('Request_price', 'Request_amount', ),
                     css_class='unsort'
                     ),
            Fieldset('实际服务内容',
                     Row('Request_actinitdate', 'Request_actinittime', ),
                     Row('Request_actenddate', 'Request_actendtime', ),
                     Row('Request_actduration', 'Request_actquantity', ),
                     Row('Request_actprice', 'Request_actamount', ),
                     css_class='unsort'
                     ),
        ),
        Side(
            Fieldset('操作参考信息',
                     'Request_comments', 'Request_status','Request_isyes',
                     ),
        )
    )
    #
# PSM add for Data filter by BU
    def queryset(self):
        qs = super(RequestBackwardAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs.filter(Request_status__in=['10','20','30'], Request_cancel__exact= False)
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu_id=account_bu, Request_status__in=['10', '20', '30'],Request_cancel__exact= False, Data_backer_id__exact=self.request.user.id)
    #
    def save_models(self):
        obj = self.new_obj
        #
        backward = obj.Request_isyes
        obj.Data_datetime = datetime.datetime.now()
        if backward is True:
            rm = RequestMaster.objects.filter(Data_bu=obj.Data_bu, Dummy_id=obj.Dummy_id).first()
            if rm:
                if obj.Request_status < rm.Request_status:
                    obj.Request_comments += '已回退！' + 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
                    obj.Request_isyes = False
                    obj.save()
                    messages.info(self.request, str(obj.Dummy_id + '回退操作已经完成'))
        if backward is False:
            obj.Request_comments += '没回退！' + 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
            obj.Request_isyes = False
            obj.save()
            messages.info(self.request, str(obj.Dummy_id + '没有进行回退操作'))
        else:
            rm = RequestMaster.objects.filter(Data_bu=obj.Data_bu, Dummy_id=obj.Dummy_id).first()
            if rm:
                if obj.Request_status > rm.Request_status:  # 回退操作不能变为前进
                    obj.Request_status = rm.Request_status
                    obj.Request_isyes = False
            obj.Request_comments += 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
            super(RequestBackwardAdmin, self).save_models()
            messages.info(self.request, str(obj.Dummy_id + '回退状态大于等于当前状态，不做更改'))
xadmin.site.register(RequestBackward, RequestBackwardAdmin)
# 工作流 pause
class RequestPauseAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    prepopulated_fields = {'slug': ('Request_desc',)}
    list_display = (
        'Dummy_id', 'Request_type', 'Request_desc', 'Request_customer', 'Request_opportunity', 'Request_project',
        'Request_usage', 'Request_cancel', 'Request_status',)
    exclude = ('')
    list_display_links = ('Dummy_id',)
    search_fields = ('Request_desc', 'Dummy_id',)
    list_filter = ['Request_opportunity', 'Request_project', 'Request_customer']
    list_export_fields = ('Request_type', 'Request_desc',)
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-save'
    save_as = False
    save = False
    remove_permissions = ('delete', 'add')
    show_bookmarks = False
    use_related_menu = False
    #hidden_menu = True
    #
    fields = ['Dummy_id', 'Request_type', 'Request_desc', 'Request_account', 'Request_comments','Request_mainresource','Request_auxresource','Request_basecompetence',
              'Request_duration', 'Request_initdate', 'Request_enddate', 'Request_inittime', 'Request_endtime', 'Request_request', 'Request_nextrequest',
              'Request_customer', 'Request_contact', 'Request_opportunity', 'Request_project', 'Request_serviceitem',
              'Request_quantity', 'Request_price', 'Request_amount', 'Request_flowcycle', 'Request_usage',
              'Request_isyes', 'Request_actinitdate', 'Request_actenddate', 'Request_actinittime', 'Request_actendtime', 'Request_actduration',
              'Request_actquantity','Request_status',
              'Request_actprice', 'Request_actamount', ]
    readonly_fields = ('Dummy_id', 'Request_type', 'Request_desc', 'Request_account',
                       'Request_flowcycle', 'Request_usage', 'Request_request', 'Request_nextrequest',
                       'Request_customer', 'Request_contact', 'Request_opportunity', 'Request_project',
                       'Request_serviceitem', 'Request_initdate', 'Request_enddate', 'Request_inittime', 'Request_endtime', 'Request_duration',
                       'Request_quantity', 'Request_price', 'Request_amount',
                       'Request_actinitdate', 'Request_actenddate', 'Request_actinittime', 'Request_actendtime','Request_actduration', 'Request_actquantity',
                       'Request_actprice', 'Request_actamount','Request_status',)
    form_layout = (
        Main(
            Fieldset('基本信息',
                     Row('Dummy_id', 'Request_usage', ),
                     Row('Request_flowcycle', 'Request_type', ),
                     Row('Request_desc', 'Request_account', ),
                     ),
            Fieldset('相关要素',
                     Row('Request_customer', 'Request_contact', ),
                     Row('Request_opportunity', 'Request_project', ),
                     Row('Request_mainresource', 'Request_auxresource',),
                     Row('Request_request', 'Request_nextrequest', ),
                     css_class='unsort'
                     ),
            Fieldset('计划服务内容',
                     Row('Request_initdate', 'Request_inittime', ),
                     Row('Request_enddate', 'Request_endtime', ),
                     Row('Request_serviceitem', ),
                     Row('Request_duration', 'Request_quantity', ),
                     Row('Request_price', 'Request_amount', ),
                     css_class='unsort'
                     ),
            Fieldset('实际服务内容',
                     Row('Request_actinitdate', 'Request_actinittime', ),
                     Row('Request_actenddate', 'Request_actendtime', ),
                     Row('Request_actduration', 'Request_actquantity', ),
                     Row('Request_actprice', 'Request_actamount', ),
                     css_class='unsort'
                     ),
        ),
        Side(
            Fieldset('操作参考信息',
                     'Request_comments', 'Request_status','Request_isyes',
                     ),
        )
    )
    #
# PSM add for Data filter by BU
    def queryset(self):
        qs = super(RequestPauseAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs.filter(Request_cancel__exact=False, Request_status__gt ='')
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu_id=account_bu, Request_cancel__exact=False, Request_status__gt ='', Data_deleter_id__exact=self.request.user.id)
    #
    def save_models(self):
        obj = self.new_obj
        #
        pause = obj.Request_isyes
        obj.Data_datetime = datetime.datetime.now()
        if pause is True:
            obj.Request_comments += '已暂停！' + 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
            obj.Request_cancel = True
            obj.save()
            messages.info(self.request, str(obj.Dummy_id + '暂停操作已经完成'))
        if pause is False:
            obj.Request_comments += '没暂停！' + 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
            obj.Request_cancel = False
            obj.save()
            messages.info(self.request, str(obj.Dummy_id + '没有进行暂停操作'))
        else:
            obj.Request_comments += 'by:' + self.request.user.username + '@' + str(obj.Data_datetime)
            super(RequestPauseAdmin, self).save_models()
xadmin.site.register(RequestPause, RequestPauseAdmin)
