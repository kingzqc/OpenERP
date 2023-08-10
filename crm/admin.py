#
import xadmin
from workflow.views import *
from django.utils.html import format_html

from django.contrib import messages
from django.shortcuts import render,redirect
from django.db.models import Q
from xadmin.views.base import get_account_bu  # psm add for get BU
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
# Register your models here.
#
# 联系人管理
class ContactMasterAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    prepopulated_fields = {'slug': ('Contact_name',)}
    list_display = ('Contact_code', 'Contact_name','colored_Contact_source', 'namecardpicture',)
    exclude = ('')
    list_display_links = ('Contact_code',)
    search_fields = ('Contact_name', 'Contact_content')
    list_export_fields = ('Contact_name', 'Contact_content')
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    #style_fields ={'Data_owner':'fk-ajax'} # manytomany fields only
    actions = ['test1','test2']
    model_icon = 'fa fa-heart-o'
    save_as = False
    #remove_permissions = ('delete', 'add')
    show_bookmarks = False
    use_related_menu = False
    #
    fields = ['Data_bu', 'Contact_code', 'Contact_name', 'Contact_source', 'Contact_method', 'Contact_content',
              'Contact_card', 'Data_owner', 'Data_creator', 'Data_security', 'Contact_status',
              'Contact_scanflag',]
    readonly_fields = ('Contact_status', 'Data_owner','Data_bu', 'image_url')
    form_layout = (
        Main(
            Fieldset('名片信息',
                     Row('Contact_card', 'Contact_scanflag', )
                     ),
            Fieldset('基本信息',
                     'Data_bu', 'Contact_code', 'Contact_name', 'Contact_source', 'Contact_method',
                     'Contact_content', css_class='unsort'
                     ),
            Fieldset('信息',
                     Row('Data_owner','Data_creator'),
                     ),
        ),
        Side(
            Fieldset('附加信息',
                     'Data_security', 'Contact_status',
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
    # PSM end for default BU
    def has_add_permission(request):
        return True

    def get_readonly_fields(self):
        if not self.org_obj:  # 新建时
            readonly_fields = []
            return readonly_fields
        else:
            readonly_fields = ['Data_bu',]  # 修改时
            return readonly_fields

# PSM add for Data filter by BU
    def queryset(self):
        ###  GET ACCOUNT BU  ###
        account_bu = get_account_bu(self)
        #########################
        qs = super(ContactMasterAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(Data_bu=account_bu)

    # 自定义屏幕列表字段
    def colored_Contact_source(self, obj):
        color_code = ''
        if 'Camp' == obj.Contact_source:
            color_code = 'green'
        elif 'S' == obj.Contact_source:
            color_code = 'red'
        elif 'A' == obj.Contact_source:
            color_code = 'black'

        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            obj.Contact_source,
        )

    colored_Contact_source.short_description = u'来源'

    # 列表显示图片方法,return 返回的是图片的地址
    def namecardpicture(self, obj):
        return '<img src="/medias/%s" height="30" width="60" />' % (obj.Contact_card)

    namecardpicture.short_description = '名片缩略图'
    namecardpicture.allow_tags = True
    # 自定义一个字段
    def image_url(self, obj):
        image = obj.Contact_card
        if self.org_obj:
            data = '{"name": "%s", "icon": "fas fa-user-tie", "url": "/base/make_bu_valid/"}' % (obj.Contact_code)
            btn2 = f"""<button οnclick='self.parent.app.openTab({data})'
                                             class='el-button el-button--danger el-button--small'>新标签</button>"""
            return mark_safe(f"<div> {btn2}</div>")
        else:
            html = "-"
            return mark_safe(html)  # 取消转义

    image_url.short_description = "反馈图片"
    image_url.allow_tags = True
#
xadmin.site.register(ContactMaster, ContactMasterAdmin)


class CustomerMasterAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    fields = ['Data_bu', 'Customer_code', 'Customer_name', 'Customer_address','Customer_source','Customer_industry',
              'Customer_scale', 'Customer_service', 'Customer_contact1', 'Customer_contact2',
              'Data_security','Customer_status','Data_owner', 'Data_secondowner', 'Data_creator']
    list_display = ('Customer_code', 'Customer_name','Customer_status','Customer_source',)
    exclude = ('')
    list_display_links = ('Customer_code',)
    search_fields = ('Data_bu__BU_code', 'Customer_name', 'Customer_address')
    list_filter = ['Data_owner_id']
    list_export_fields = ('Customer_name', 'Customer_address')
    relfield_style = 'level'  # 带有外键的字段变成搜索格式
    actions = ['test1','test2']
    model_icon = 'fa fa-user'
    save_as = False
    show_bookmarks = False
    use_related_menu = False
#
    form_layout = (
        Main(
            Fieldset('基本信息',
                     'Customer_code', 'Customer_name', 'Customer_address', css_class='unsort',
                     ),
            Fieldset('分类信息',
                     Row('Customer_source','Customer_industry'),
                     Row('Customer_scale', 'Customer_service'),
                     ),
            Fieldset('联系信息',
                     'Customer_contact1', 'Customer_contact2',
                     ),
        ),
        Side(
            Fieldset('权属信息',
                     'Data_bu', 'Data_security', 'Customer_status','Data_owner', 'Data_secondowner', 'Data_creator',
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
    def queryset(self):
        ###  GET ACCOUNT BU  ###
        account_bu = get_account_bu(self)
        #########################
        qs = super(CustomerMasterAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(Q(Data_owner__exact=self.request.user.id) | Q(Data_secondowner__exact=self.request.user.id), Data_bu=account_bu)
    #
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
        if db_field.name == 'Customer_industry':
            kwargs["queryset"] = BuParameter.objects.filter(Bu_paratype='industry')
            #kwargs["widget"] = RadioSelect
        if db_field.name == 'Customer_scale':
            kwargs["queryset"] = BuParameter.objects.filter(Bu_paratype='scale')
            #kwargs["widget"] = RadioSelect
        if db_field.name == 'Customer_service':
            kwargs["queryset"] = BuParameter.objects.filter(Bu_paratype='service')
            #kwargs["widget"] = RadioSelect
        return db_field.formfield(**dict(**kwargs))

xadmin.site.register(CustomerMaster, CustomerMasterAdmin)

# 商机维护
class OpportunityMasterAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    fields =['Opportunity_source', 'Opportunity_code', 'Opportunity_name',
                'Opportunity_contact', 'Opportunity_customer',
                'Opportunity_initialamount', 'Opportunity_currentamount',
                'Opportunity_finalamount', 'Opportunity_serviceitem',
                    'Opportunity_nowstage', 'Opportunity_nextstage',
                 'Opportunity_flowcycle','Opportunity_nowstage', 'Opportunity_nextstage',
                    'Opportunity_status',
                    'Data_bu', 'Data_security', 'Data_owner', 'Opportunity_ownershare', 'Data_secondowner', 'Opportunity_secondshare','Data_creator', 'Data_approver',]
    list_display = ('Opportunity_code', 'Opportunity_name', 'Opportunity_source', 'Opportunity_serviceitem', 'Opportunity_nowstage', 'Opportunity_nextstage', 'Opportunity_status')
    exclude = ('')
    list_display_links = ('Opportunity_code',)
    search_fields = ('Opportunity_name','Data_owner_id__id')
    list_filter = ['Data_bu', 'Data_owner_id']
    list_export_fields = ('Opportunity_name', 'Opportunity_source')
    show_detail_fields = ['Data_bu']
    #relfield_style = 'fk-ajax'  # 带有外键的字段变成搜索格式
    actions = ['test1', 'test2']
    model_icon = 'fa fa-circle-o'
    save_as = False
    show_bookmarks = False
    use_related_menu = False
    #
    form_layout = (
        Main(
            Fieldset('流程状态',
                     'CurrentStage',
                     ),
            Fieldset('基本信息',
                     Row('Opportunity_source', 'Opportunity_code',),
                     'Opportunity_name',
                     ),
            Fieldset('标的信息',
                     Row('Opportunity_contact', 'Opportunity_customer',),
                     Row('Opportunity_initialamount', 'Opportunity_currentamount',),
                     Row('Opportunity_finalamount', 'Opportunity_serviceitem',),
                     ),
            Fieldset('流程关联',
                     Row('Opportunity_flowcycle', 'flowcycle_content',),
                     Row('Opportunity_nowstage', 'Opportunity_nextstage', ),
                     ),
        ),
        Side(
            Fieldset('权属信息',
                     'Data_bu', 'Opportunity_status','Data_security', 'Data_owner','Opportunity_ownershare', 'Data_secondowner','Opportunity_secondshare', 'Data_creator', 'Data_approver',
                     ),
        ),
    )

    def ResetAuth(self):
        # 重新定义此函数，限制普通用户的增删改权限
        if self.user.is_superuser:
            self.remove_permissions = ()
        return self.remove_permissions

    remove_permisson = ('delete',)

    #    remove_permissions = ('delete', 'add', 'change'，'view')
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
    def get_readonly_fields(self):
        if not self.org_obj:  # 新建时
            readonly_fields = []
            return readonly_fields
        else:
            if self.org_obj.Opportunity_status =='OPEN':
                readonly_fields = ['Opportunity_source', 'Opportunity_code', 'Opportunity_name',
                'Opportunity_contact', 'Opportunity_customer', 'flowcycle_content',
                'CurrentStage',
                'Opportunity_initialamount', 'Opportunity_currentamount','Opportunity_nowstage', 'Opportunity_nextstage',] # 修改时

                exclude = ('Opportunity_initialamount', 'Opportunity_currentamount')
            else:
                readonly_fields = ['Data_bu', 'flowcycle_content', 'CurrentStage',]  # 修改时
            return readonly_fields
    #
    def queryset(self):
        qs = super(OpportunityMasterAdmin,self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu=account_bu, Data_owner_id=self.request.user.id)
    #
    def formfield_for_dbfield(self, db_field, **kwargs):
       #
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        account_bu = get_account_bu(self)
        if db_field.name == 'Opportunity_serviceitem':
            kwargs["queryset"] = ItemMaster.objects.filter(Data_bu=account_bu)
        if db_field.name == 'Opportunity_flowcycle':
            kwargs["queryset"] = FlowType.objects.filter(Data_bu=account_bu, Flowtype_usage ='CRM')
        return db_field.formfield(**dict(**kwargs))
    #
    def save_models(self):
        obj = self.new_obj
        if not obj.Opportunity_flowcycle:

            messages.info(self.request, 'opppp')
            obj.save()
        else:
            super(OpportunityMasterAdmin, self).save_models()
    #
    def flowcycle_content(self, obj):
        print
        typelist = FlowCycleMaster.objects.filter(Data_bu=obj.Data_bu, Flowcycle_type_id=obj.Opportunity_flowcycle_id)
        flow_content =''
        for type in typelist:
            if flow_content != '':
                flow_content = str(flow_content) + '->' + str(type.Flowcycle_stagedesc)
            else:
                flow_content = str(type.Flowcycle_stagedesc)
        return flow_content
    flowcycle_content.short_description = '内容'
    # 获取商机的各工作流当前状态
    def CurrentStage(self,obj):
        stage =''
        typelist = FlowCycleMaster.objects.filter(Data_bu=obj.Data_bu, Flowcycle_type_id=obj.Opportunity_flowcycle_id)
        for type in typelist:
            rm = RequestMaster.objects.filter(Request_opportunity_id=obj.Data_id, Request_type_id=type.Flowcycle_stage).first()
            if rm:
                stage = stage + '['+ str(type.Flowcycle_stagedesc) +']' + '流程['+ str(rm.Dummy_id)+']状态['+str(rm.Request_status)+'];'

        return format_html(stage)
    CurrentStage.short_description = '概述：'
    #
xadmin.site.register(OpportunityMaster, OpportunityMasterAdmin)
# 商机批准
class OpportunityApproveAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    list_display = ('Opportunity_code', 'Opportunity_name', 'Opportunity_source', 'Opportunity_serviceitem',
                    'Opportunity_nowstage', 'Opportunity_nextstage', 'Opportunity_status')
    exclude = ('')
    #
    fields =['Opportunity_source', 'Opportunity_code', 'Opportunity_name',
                'Opportunity_contact', 'Opportunity_customer',
                'Opportunity_initialamount', 'Opportunity_currentamount',
                'Opportunity_finalamount', 'Opportunity_serviceitem',
                 'Opportunity_flowcycle','Opportunity_nowstage', 'Opportunity_nextstage',
                    'Opportunity_status', 'Opportunity_comments', 'Data_datetime',
                    'Data_bu', 'Data_security', 'Data_owner', 'Opportunity_ownershare', 'Data_secondowner', 'Opportunity_secondshare',]
    #
    readonly_fields = ['Opportunity_source', 'Opportunity_code', 'Opportunity_name','Opportunity_contact', 'Opportunity_customer',
                       'Opportunity_initialamount', 'Opportunity_currentamount','Opportunity_finalamount', 'Opportunity_serviceitem',
                    'Opportunity_nowstage', 'Opportunity_nextstage','Opportunity_flowcycle',
                 'Data_datetime', 'Data_bu', 'Data_security', 'Data_owner', 'Data_secondowner', 'Opportunity_ownershare','Opportunity_secondshare',]
    list_display_links = ('Opportunity_code',)
    search_fields = ('Opportunity_name','Data_owner_id__id')
    list_filter = ['Data_bu', 'Data_owner_id']
    list_export_fields = ('Opportunity_name', 'Opportunity_source')
    show_detail_fields = ['Data_bu']
    #relfield_style = 'fk-ajax'  # 带有外键的字段变成搜索格式
    model_icon = 'fa fa-circle-o'
    save_as = False
    save_as_continue = False
    remove_permissions = ('delete','add')
    show_bookmarks = False
    use_related_menu = False
    form_layout = (
        Main(
            Fieldset('基本信息',
                     Row('Opportunity_source', 'Opportunity_code',),
                     'Opportunity_name',
                     ),
            Fieldset('标的信息',
                     Row('Opportunity_contact', 'Opportunity_customer',),
                     Row('Opportunity_initialamount', 'Opportunity_currentamount',),
                     Row('Opportunity_finalamount', 'Opportunity_serviceitem',),
                     ),
            Fieldset('Flow信息',
                     Row('Opportunity_flowcycle','Data_datetime',),
                     Row('Opportunity_nowstage', 'Opportunity_nextstage',),
                     ),
            Fieldset('权属信息',
                     Row('Data_bu', 'Data_security',),
                     Row('Data_owner', 'Opportunity_ownershare',),
                     Row('Data_secondowner', 'Opportunity_secondshare',),
                     ),
        ),
        Side(
            Fieldset('审批信息',
                      'Opportunity_comments','Opportunity_status',
                     ),
        ),
    )
#
    def queryset(self):
        qs = super(OpportunityApproveAdmin,self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu=account_bu, Data_approver_id=self.request.user.id)
    def formfield_for_dbfield(self, db_field, **kwargs):
       #
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        account_bu = get_account_bu(self)
        if db_field.name == 'Opportunity_serviceitem':
            kwargs["queryset"] = ItemMaster.objects.filter(Data_bu=account_bu)
        if db_field.name == 'Opportunity_flowcycle':
            kwargs["queryset"] = FlowType.objects.filter(Data_bu=account_bu, Flowtype_usage ='CRM')
        return db_field.formfield(**dict(**kwargs))
    #
    def save_models(self):
        obj = self.new_obj
        if obj.Opportunity_status and obj.Opportunity_status=='OPEN':
            # 传递参数， 生成销售周期的流程
            flow_parameter ={}
            flow_parameter['mode'] = 'CREATEFLOW'
            flow_parameter['cycle'] = str(obj.Opportunity_flowcycle_id)
            flow_parameter['opportunity'] = str(obj.Data_id)
            flow_parameter['databuid'] = str(obj.Data_bu_id)
            flow_parameter['resource'] = str(obj.Data_owner_id)
            flow_parameter['approver'] = str(obj.Data_approver_id)
            flow_parameter['contact'] = str(obj.Opportunity_contact_id)
            flow_parameter['customer'] = str(obj.Opportunity_customer_id)
            flow_parameter['item'] = str(obj.Opportunity_serviceitem_id)
            flow_parameter['amount'] = str(obj.Opportunity_initialamount)
            flow_parameter['startdate'] = str(obj.Opportunity_date)
            # wf = work flow
            wf = workflow_engine.FlowCycle_flow(self, flow_parameter)
            obj.Opportunity_nowstage = wf['nowstage']
            obj.Opportunity_nextstage = wf['nextstage']
            obj.Opportunity_status = 'APPROVED'
            obj.save()
            messages.info(self.request, wf['message'])
        else:
            super(OpportunityApproveAdmin, self).save_models()
xadmin.site.register(OpportunityApprove, OpportunityApproveAdmin)
